import logging
import base64
import cv2
import os
from json import *

import zmq
from rest_framework.response import Response
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth

from models import *
from validation import *
from config import client_req_ip, client_req_port, project_name
from proto_code import proto_encode, proto_decode
from SockMan import socket_manager
#Creat and save new images.

logging.basicConfig(format='[%(asctime)s] %(message)s', 
	level=logging.DEBUG, datefmt='%d/%b/%Y %I:%M:%S')

#global socket
client_socket = None

def Creat_Save_img(request, Project):
	new_img = Picture.objects.create(project = Project, name = request.FILES.get('img').name,
		Image = request.FILES.get('img'))
	if request.user.is_authenticated:
		new_img.uploader = request.user
	new_img.save()
	uploader_name = (new_img.uploader.username if hasattr(new_img.uploader, 'username') else 'Unknown')
	#remember to delete,
	logging.info("%s is saved.		uploader:	%s" % (new_img.Image.name, uploader_name))
	return new_img

#Home Page
def index(request):
	return render(request, 'index.html', {})

#Show local images for user to chose. Interact with jQuery codes:m_jquery_function.js
def gallery(request):
	path = request.path.split('/')
	while '' in path:
		path.remove('')
	Project = path[-2]
	root_dir = os.path.join('upload/static', Project+'_gallery')
	img_list = os.listdir(root_dir)
	#transfer to json format
	img_json_list = JSONEncoder().encode(img_list)
	logging.info("gallery images all returned to page")
	return HttpResponse(img_json_list)

#Return Page and call models to predict or segmentate.
def project(request):
	global client_socket
	context = {"display": False,}
	#socket
	if client_socket == None:
		
		request_address = "tcp://%s:%s" % (client_req_ip, client_req_port)
		client_socket = socket_manager.create_socket(zmq.Context(), zmq.REQ, request_address, server = False, passive = True)
		logging.info("connect to %s" % request_address)
	#Get the project name
	path = request.path.split('/')
	while '' in path:
		path.remove('')
	Project = path[-1]
	context = {'Project':Project}
	logging.info("Current project is %s" % (Project,))

	#When use zeromq and protobuffer,these can be deleted.
	if request.method == 'POST':
		context["display"] = True
		#to distinguish where the data comes from(gallery or upload)
		if request.FILES.has_key('img'):
			logging.info("Image come from upload.")
			new_img = Creat_Save_img(request, Project)
			IMAGE_FILE = "storage/"
			IMAGE_NAME = new_img.Image.name
			url = new_img.Image.url
		else:
			logging.info("Image come from gallery.")
			IMAGE_FILE = "upload/static/"+Project+"_gallery/"
			IMAGE_NAME = request.POST['img_name']
			url = "/static/"+Project+"_gallery/"+IMAGE_NAME

		context["img_url"] = url

		if Project == 'Diabetic':
			#send and recieve message
			send_data = proto_encode(Project, os.path.join(IMAGE_FILE, IMAGE_NAME))
			logging.info("waiting, send_data...")
			client_socket.send_multipart(send_data)
			logging.info("data_send successfully\nwaiting for reply...")
			recv_data = client_socket.recv()
			logging.info("successfully recived message from server")
			decoded_data = proto_decode(Project, recv_data)
			#render to display
			context["base64encoded"] = base64.b64encode(decoded_data[1])
			context["probility"] = str(decoded_data[2]*100)[0:6]
			context["prediction"] = decoded_data[3]
			#print "decoded_data:",decoded_data
		elif Project == 'X-Chest':
			#send and recieve message
			send_data = proto_encode(Project, os.path.join(IMAGE_FILE, IMAGE_NAME))
			logging.info("waiting, send_data...")
			client_socket.send_multipart(send_data)
			logging.info("data_send successfully\nwaiting for reply...")
			recv_data = client_socket.recv()
			logging.info("successfully recived message from server")
			decoded_data = proto_decode(Project, recv_data)
			#render to display
			context["base64encoded"]=base64.b64encode(decoded_data[1])
		else:
			print 'sorry, we have not ...'
			return render(request, 'index.html', {})
	return render(request, 'project.html', context)

def acc_profile(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/')
	imgs = Picture.objects.filter(uploader = request.user)
	context = {"username":request.user.username, "e_mail":request.user.email, 
	"profile":request.user.profile, "imgs":imgs, }
	return render(request, 'profile.html', context)

def registe(request):
	if request.method == 'GET':
		return render(request, 'registe.html', {})
	context = is_valid_registe(request)
	if context["error"] == False:
		new_user = User(username = context["username"], password = context["password"],
				email = context["email"], )
		new_user.save()
		auth.login(request, new_user)
		return render(request, 'Success.html', {"word":"Congratulations!You have succedded in registing!"})
	return render(request, 'registe.html', context)

def login(request):
	if request.method == 'GET':
		return render(request, 'login.html', {})
	context = is_valid_login(request)
	if context["error"] == True:
		return render(request, 'login.html', context)
	auth.login(request, context["USER"])
	return HttpResponseRedirect('/')

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

def change_password(request):
	if request.method == 'GET':
		return render(request, 'change_password.html', {})
	if request.method == 'POST':
		context = password_valid(request)
		if context["error"] == True:
			return render(request, 'change_password.html', context)
		request.user.password = request.POST["newpassword1"]
		request.user.save()
		return render(request, 'Success.html', {"word":"You have changed your password successfully!"})

from models import *
from django.template import Context
import re

def is_valid_registe(request):

	context = {"username":"", "email":"", "name_exist":False, 
	"name_type_error":False, "password_type_error":False,
	"email_exist":False, "email_type_error":False, "password":"", "error":False}
	
	name_type = r'[^0-9a-zA-Z@+-._]'
	email_type = r'^(\w)+(\.\w+)*@(\w)+((\.\w{2,3}){1,3})$'
	password_type = r'[^0-9a-zA-Z@+-._]'
	if request.method == 'GET':
		return context
	if request.method == 'POST':
		error = False
		if request.POST["username"]:
			context["username"] = request.POST["username"]
			if User.objects.filter(username = request.POST["username"]):
				context["name_exist"] = True
			elif len(request.POST["username"]) < 4 or re.match(name_type,request.POST["username"]):
				context["name_type_error"] = True
		else:
			context["name_type_error"] = True
		if request.POST["password"]:
			context["password"] = request.POST["password"]
			if len(request.POST["password"]) < 4 or re.match(password_type,request.POST["password"]):
				context["password_type_error"] = True
		else:
			context["password_type_error"] = True
		if request.POST["email"]:
			context["email"] = request.POST["email"]
			if User.objects.filter(email = request.POST["email"]):
				context["email_exist"] = True
			elif re.match(email_type,request.POST["email"]) == None:
				context["email_type_error"] = True
		else:
			context["email_type_error"] = True
		context["error"] = context["name_exist"] or context["name_type_error"] or context["email_exist"] or context["email_type_error"] or context["password_type_error"]
		return context
def is_valid_login(request):

	context = {"error":False,}
	
	if request.method == 'POST':
		if request.POST["username"] and request.POST["password"]:
			find_user=User.objects.filter(username = request.POST["username"])
			if find_user:
				for user in find_user:
					if user.password == request.POST["password"]:
						context["USER"] = user
				if not context.has_key("USER"):
					context["error"] = True
			else:
				context["error"] = True
		else:
			context["error"] = True
		
		return context
def password_valid(request):
	context = {"old_error":False, "new_type_error":False, "consistency_error":False,"error":False}
	password_type = r'[^0-9a-zA-Z@+-._]'
	if request.POST["oldpassword"]:
		if request.POST["oldpassword"] != request.user.password:
			context["old_error"] = True
	else:
		context["olde_rror"] = True
	if request.POST["newpassword1"]:
		if len(request.POST["newpassword1"]) < 4 or re.match(password_type,request.POST["newpassword1"]):
			context["new_type_error"] = True
	else:
		context["new_type_error"] = True
	if request.POST["newpassword1"] != request.POST["newpassword2"]:
		context["consistency_error"] = True
	context["error"] = context["old_error"] or context["new_type_error"] or context["consistency_error"]
	return context
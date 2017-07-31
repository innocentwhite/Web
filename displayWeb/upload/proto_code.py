import numpy as np
import cv2
# import cPickle as pickle
# import zlib
import logging
import time

import engmsg2_pb2
from config import client_version

def proto_encode(project, img_fname):
	logging.info("start encode message...")
	time_start = time.time()

	if project == "Diabetic":
		req = engmsg2_pb2.DiabeticRequest()
		req_code = engmsg2_pb2.REQ_Diabetic
	elif project == "X-Chest":
		req = engmsg2_pb2.XChestSegRequest()
		req_code = engmsg2_pb2.REQ_XChestSeg
	else:
		return None

	req.client_version = client_version
	req.datatype = engmsg2_pb2.ORIG

	#request img serialize and compress
	with open(img_fname, "rb") as f:
		buf = f.read()
	req.img = buf

	data = req.SerializeToString()

	time_used = int((time.time() - time_start) * 1000)
	logging.info("encode finished.	encode time_used: %sms" % (time_used, ))

	return [str(req_code), data]

def proto_decode(project, recv_data):
	logging.info("start decode message...")
	time_start = time.time()

	if project == "Diabetic":
		reply = engmsg2_pb2.DiabeticReply()
	elif project == "X-Chest":
		reply = engmsg2_pb2.XChestSegReply()
	else:
		return None

	reply.ParseFromString(recv_data)

	time_used = int((time.time() - time_start) * 1000)
	logging.info("decode finished.	decode time_used: %sms" % (time_used, ))

	if project == "Diabetic":
		#decompress and deserialize
		# img_ser = zlib.decompress(reply.preprocessed)
		# img_array = pickle.loads(img_ser)
		
		return [reply.header, reply.preprocessed, reply.prob, reply.severity]
	elif project == "X-Chest":
		#decompress and deserialize
		# img_ser = zlib.decompress(reply.labelled_img)
		# img_array = pickle.loads(img_ser)

		return [reply.header, reply.labelled_img]
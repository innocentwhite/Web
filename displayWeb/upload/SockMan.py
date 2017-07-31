import zmq

class socket_manager:

	def __init__(self):
		pass
		# TYPE = zmq.ROUTER if server else zmq.REQ
		# self.socket = context.socket(TYPE)
		# if passive and server:
		# 	self.socket.connect(listen_addr)
		# else:
		# 	self.socket.bind(listen_addr)

	@staticmethod
	def create_socket(context, TYPE, listen_addr, server, passive = True):
		socket = context.socket(TYPE)
		port = listen_addr.split(':')[-1]
		local = "tcp://*:%s" % (port, )
		if (passive ^ server):
			socket.bind(local)
		else:
			socket.connect(listen_addr)
		return socket

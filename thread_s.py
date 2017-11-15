# command : python thread_s.py

import socket
import os
import threading, time

host = '127.0.0.1'
port = 8080
webport = 80
client = []
thd = []
cnt = 0

def proxy(conn):
	while True:
		data = conn.recv(1024)
		if not data:
			continue
	
		sp = data.find('GET' or 'POST' or 'HEAD' or 'PUT' or 'DELETE' or 'OPTIONS') 
		if sp == -1: 	# if not HTTP REQUEST
			continue
		webhost = str(data.split()[4])
		#print 'webhost', webhost
	
		ndata = "GET http://google.com/ HTTP/1.1\x0d\x0a" 
		ndata += "Host: google.com\x0d\x0a"
		
		data = ndata + data	
		print 'new data : \x0d\x0a', data	
		
		r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		r.connect((webhost, webport))
		print '===Connect to server==='
		
		r.send(data)
		
		time.sleep(1)

		resp = r.recv(1024)
		if not resp:
			continue

		'''snd = resp.rfind('HTTP/1.1')
		print 'snd :', snd
		if snd == 0:
			conn.send(resp)
			print 'HTTP response :', resp
			conn.send(resp)
	
		else:
			resp1 = resp[0:snd-1]
			resp2 = resp[snd:]

			print 'HTTP response :', resp1
			print 'HTTP response2 :', resp2
		
			conn.send(resp2)'''

		respp = r.recv(1024)	
		if not respp:
			print 'HTTP response :', resp
			conn.send(resp)
			continue
		print 'HTTP response :', resp
		print 'HTTP response2 :', respp

		conn.send(respp)
		conn.close()
	

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(1)

while True:
	print 'connecting to client...'
	conn, addr = s.accept()
	client.append(conn)
	cnt += 1
	print 'connected by', addr, 'client', cnt

	t = threading.Thread(target=proxy, args=(conn,))
	t.start()
	thd.append(t)

for i in thd:
	i.join()


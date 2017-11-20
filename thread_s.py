import socket
import os
import threading, time

host = '127.0.0.1'
port = 8080
webport = 80
client = []
thd = []
cnt = 0
plen = 10000

def proxy(conn):
	while True:
		data = conn.recv(plen)
		if not data:		# no data
			continue
	
		sp = data.find('GET' or 'POST' or 'HEAD' or 'PUT' or 'DELETE' or 'OPTIONS') 
		if sp == -1: 	# if not HTTP REQUEST
			continue
		webhost = str(data.split()[4])
		#print 'webhost', webhost
	
		ndata = "GET http://google.com/ HTTP/1.1\x0d\x0a" 
		ndata += "Host: google.com\x0d\x0a\x0d\x0a"
		#ndata = "GET / HTTP/1.1\x0d\x0a" 
		#ndata += "Host: dummy.com \x0d\x0a\x0d\x0a"
		
		data = ndata + data	
		print 'new data : \x0d\x0a', data	
		
		r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		r.connect((webhost, webport))
		print '===Connect to server==='
		
		r.send(data)
		
		time.sleep(1)

		resp = r.recv(plen)
		if not resp:
			continue
		# connect -> webhost == response_host check
		if (resp.count('HTTP/1.1') > 1):
			print 'count :', resp.count('HTTP/1.1')
			snd = resp.rfind('HTTP/1.1')
			print 'snd :', snd
			
			resp1 = resp[0:snd-1]
			resp2 = resp[snd:]

			print 'HTTP response :', resp1, '\x0d\x0a'
			print 'HTTP response2 :', resp2
		
			conn.send(resp2)
		else:
			'''respp = r.recv(plen)	
			if not respp:		# no data
				print 'HTTP response :', resp
				continue
			print 'HTTP response :', resp, '\x0d\x0a'
			print 'HTTP response2 :', respp

			conn.send(respp)'''
			
			i=0		
			while True:
				respp = r.recv(plen)			
				if not respp:
					print 'final packet num :', i
					break

				if i == 0:
					conn.send(resp)			
					conn.send(respp)
					print 'HTTP response', i, '\x0d\x0a', resp, '\x0d\x0a'
					print 'HTTP response', i, '\x0d\x0a', respp, '\x0d\x0a'
				else:
					conn.send(respp)			
					print 'HTTP response', i, '\x0d\x0a', respp, '\x0d\x0a'
				i = i+1		
	
	
		conn.close()
	

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(10)

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


import requests

#payload = {'username': 'victor', 'password': 'great'}
r = requests.get('https://httpbin.org/basic-auth/victor/great',auth=('victor', 'great'))
#r = requests.get('https://httpbin.org/get', params=payload)
#print(r) displays 200
#print(dir(r)) displays the  all detils contain in the  url
#print(help(r)) diplays the  show the whole info about th url
#print(r.content)
#print(r.text)
#with open('1595863239.png', 'wb') as f:
 #f.write(r.content)
#print(r.headers)
#print(r.text) #r = requests.get('https://httpbin.org/get', params=payload)
#print(r.text) r = requests.post('https://httpbin.org/post', data=payload)
#r_dict = r.json
#(r_dict = r.json()
#print(r_dict['form']) {'password': 'great', 'username': 'victor'}
#print(r_dict['headers']) {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Content-Length': '30', 'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.32.3'
#, 'X-Amzn-Trace-Id': 'Root=1-68643f27-7e05fad731ec7c445ed63fa4'})
#print(r.text) r = requests.get('https://httpbin.org/basic-auth/victor/great', timeout= 3, auth=('victo>



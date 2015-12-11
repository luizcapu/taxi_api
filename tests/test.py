__author__ = 'luiz'

from requests import put, get, post

url = 'http://localhost:5000/driver'
post_url = '/status'

print post(url+'/123'+post_url, data={'status':'{"available": true, "location": {"lat":10, "lon":20}}'})

print put(url+'/todo1'+post_url, data={'data': 'Remember the milk'}).json()
print get(url+'/todo1'+post_url).json()
print put(url+'/todo2'+post_url, data={'data': 'Change my brakepads'}).json()
print get(url+'/todo2'+post_url).json()

print get(url+'/todo1'+post_url)
print get(url+'/todo2'+post_url)

#for this to work, have to install pip (library manager for python)
#and go like pip install requests 

import requests, json
URL = 'http://38.88.75.83/db/uploadfile2.php'
URL1 = 'http://38.88.75.83/db/createuser.php'
myfile = './test.txt'

#r=open for reading, b=open as binary
files = {'UploadFileField':open(myfile, 'rb') } 
r = requests.post(URL, files = files);

values = {
	'username' : 'hello123',
	'password' : 'hello123'
}

req = requests.post(URL1, data = values)

print(r.text)
print(req.text)

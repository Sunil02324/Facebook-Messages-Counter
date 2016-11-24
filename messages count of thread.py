import requests
import json
from time import sleep

## We had proxy enabled in our institute. Comment the below lines if not needed.
http_proxy  = "http://host:port"
https_proxy = "https://host:port"
proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy
    }

## Select any of your conversation ID from here https://developers.facebook.com/tools/explorer/145634995501895/?method=GET&path=me%2Finbox&version=v2.2
## Replace the <conversationID> and access_token from your Graph API explorer
##URL for the converstaion : https://graph.facebook.com/v2.2/<conversationID>?access_token=###
## Please note that Profile ID and Cnversation ID are not same. 
url = '###'

first = True
loop = True
requests_count = 0
peoples = []
ids = []
count = 0

resp = requests.get(url,proxies=proxyDict)
data = resp.json()
try:
	mums = data['to']['data']
	for mum in mums:
		peoples.append(mum['name'])
		ids.append(mum['id'])
		count += 1
	sleep(1)
except:
    print "Response does not contain 'data', here is what Response looks like:"
    print data 
    sleep(20)

messages_count = [0]*count

##Used Sleep several times to escape from the API rate limiting. 
##There might be some cases of Access Token Expiration. In that case, decrease the time of sleep.
while loop:
	try:
		print requests_count
		resp = requests.get(url,proxies=proxyDict)
		if first:
			data = resp.json()
			try:
				messages = data['comments']['data']
				for message in messages:
					for i in range(0,count):
						if message['from']['id'] == ids[i]:
							messages_count[i] = int(messages_count[i]) + 1
							break
				url = data['comments']['paging']['next']
				first = False
				requests_count += 1
				sleep(0.5)
			except:
			    print "Response does not contain 'data', here is what Response looks like:"
			    print data 
			    sleep(20)
		else:
			data1 = resp.json()
			try:
				if(data1['data']):
					messages = data1['data']
					for message in messages:
						for i in range(0,count):
							if message['from']['id'] == ids[i]:
								messages_count[i] = int(messages_count[i]) + 1
								break
					url = data1['paging']['next']
					requests_count += 1
					sleep(0.5)
				else:
					loop = False
			except:
			    print "Response does not contain 'data', here is what Response looks like:"
			    print data1 
			    for i in range(0,count):
			    	print "Messages Sent By " + str(peoples[i]) + " : " + str(messages_count[i])
			    sleep(20)
	except IOError as e:
		print "Socket error. Sleeping for 2 seconds"
		sleep(2)
		continue
	except requests.exceptions.ConnectionError as e:
		print "Proxy Error. Sleeping for 2 seconds"
		sleep(2)
		continue


## Printing the Member names and there messages count respectively.
for i in range(0,count):
	print "Messages Sent By " + str(peoples[i]) + " : " + str(messages_count[i])
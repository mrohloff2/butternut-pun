import requests

def getCookie(addr) :

	url = "https://"+ addr + "api/aaaLogin.json"
	
	payload= {"aaaUser" :
		  {"attributes" :
		  	{"name" : "cisco",
		  	 "pwd" : "cisco"}
		  }
	}
	
	response = requests.ost(url, json=payload, verfiy = False)
	
	return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]
	
address = '10.10.20.177'


cookie = getCookie(address)	
	

	

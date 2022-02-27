
import requests

def check_link(url):
	"""
	vrátí http kód odpovědi na url stránku a zprávu k ní příslušnou
	"""
	req = requests.get(url)						#pošleme request na zadanou 
	status = req.status_code					#extrahujem http kód odpovědi
	message = req.text							#extrahujem text http odpovědi
	if str(status)[0]=="2":
		return(f"link functional, status code {status}")	#máme funkční odkaz

	if str(status)=="400":
		return(f"bad request {status}")			#error 400 často vrací dlouhou zprávo, proto vyjímka
	if str(status)=="404":
		return(f"site not found {status}")		#error 404 často vrací dlouhou zprávo, proto vyjímka
	if str(status)=="403":
		return(f"Forbidden {status}")			#error 403 často vrací dlouhou zprávo, proto vyjímka
	if str(status)=="503":
		return(f"Service Unavailable {status}")	#error 503 často vrací dlouhou zprávo, proto vyjímka

	else:
		return(f"{message} {status}")			#pokud nemáme běžný error, vrátíme cokoliv jiného máme

def return_status_code(url):
	"""
	vrací pouze http kód odpovědi na zadanou url
	"""
	req = requests.get(url)
	status = req.status_code
	return status



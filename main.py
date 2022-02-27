import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin
from pprint import pprint

"""
import sys
"""
from broken_links import check_link, return_status_code
"""
web = "https://ksvi.mff.cuni.cz/~holan/"
max_depth = 1

web = sys.argv[1]
max_depth = int(sys.argv[2])
"""

try:
	web = str(input("zadejte celou adresu webu, tedy např. https://google.com\n"))
	requests.get(web).status_code == 200
except requests.exceptions.MissingSchema:
	print("nebyla zadána validní webová stránka, zkuste to znovu")
	web = str(input("zadejte celou adresu webu, tedy např. https://google.com\n"))


try:
	print("pokud zadáte hloubku > 2, pak je možné že program bude běžet velmi dlouho, > 10 minut")
	max_depth = int(input("zadejte hloubku, do které chcete prohledávat\n"))
except ValueError:
	print("nebyla zadána hodnota typu <int>, zkuste znovu\n")
	max_depth = int(input("zadejte hloubku, do které chcete prohledávat\n"))



def scrape_until_given_depth(web,max_depth):
	"""
	projde zadané url:web do zadané hloubky:max_depth
	"""
	visited = set([web])	#set navštívených stránek
	queue = [[web, "", 0]]	#fronta uchovávající stránky, které ještě musíme projít
	broken_links = {}		#seznam nefunkčních linku a jejich http kódů ve formátu web:kod

	while queue:			#program pracuje dokud fronta není prázdná
		url,path,depth = queue.pop(0)
		

		if depth < max_depth:
			try:
				reqs = urllib.request.urlopen(url+path).read()	#vytvoříme html dokument pomocí spojení url+path

				soup = BeautifulSoup(reqs, 'html.parser')		#předáme html do objektu BeautifulSoup, abychom s ním mohli dál pracovat

				for link in soup.find_all('a'):					#nalezneme všechny odkazy v html
					href = urljoin(url,link.get('href'))		#vybereme z odkazů pouze href část, kde je URL a přidáme ji url
					#print(href)

					if href not in visited:
						visited.add(href)						#přidáme stránku do navštívených, pokud jsme na ni ještě nebyli

						try:
							"""
							máme funkční odkaz, vypíšeme hladinu a http kód
							"""
							print("  " * depth + f"└─ at depth {depth}: {href}, {check_link(href)}")

							status_code = return_status_code(href)
							if status_code != 200:
								broken_links[href] = status_code	#přidáme nefunkční link do broken_links


						except:
							"""
							nemáme funkční odkaz, vypíšem cokoliv máme a hladinu
							"""
							print("  " * depth + f"└─ at depth {depth}: {href} -- not valid url")


					if href.startswith("http"):
						"""
						máme celou url adresu
						"""
						queue.append([href, "", depth + 1])

					else:
						"""
						nemáme celou adresu, připojíme k url
						"""
						queue.append([url, href, depth + 1])

			except urllib.error.HTTPError as out:
				"""
				expetion pro případ permanent redirectu či jiných problémů. Díky tomuto nespadne celý program
				"""
				output = format(out)
				print(output)

	return(f"unfunctional links are {broken_links}")


pprint(scrape_until_given_depth(web,max_depth))




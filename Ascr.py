import requests, sys
from bs4 import BeautifulSoup

res = requests.get(f'{sys.argv [1]}')
soup = BeautifulSoup(res.text, 'html.parser')

if "/sociation.org" in sys.argv [1]: # парсит ссылки вида "https://sociation.org/word/Слово" 
	general_title = soup.find("h1", {"id": "page-title"})
	general_words = soup.find("ol", class_="associations_list self-clear")

	title = (general_title.text).strip()
	words_list = (general_words.text).strip()

	f = open(f'{title}.txt', "x")
	f.close()
	file = open(f'{title}.txt',"r+")
	data = title +"\n"*2 + words_list

	with open(f'{title}.txt', 'r+',encoding="utf-8") as file:
		file.writelines(data)

	print(f"File saved as \"{title}\"")

else: # парсит ссылки вида "https://wordassociations.net/en/words-associated-with/Word"
	page = 0
	general_title = soup.find("h1", class_= "results-header")
	title = (general_title.text).strip()

	mega_n, mega_adj, mega_v, mega_adv = [], [], [], []

	try:
		while page <= 800:
			link = (f"{sys.argv [1]}?start={page}")
			res = requests.get(link)
			soup = BeautifulSoup(res.text, 'html.parser')
			general_nouns = list((soup.find("div", class_="section NOUN-SECTION")).strings)[1::]
			mega_n += general_nouns
			general_adjectives = list((soup.find("div", class_="section ADJECTIVE-SECTION")).strings)[1::]
			mega_adj += general_adjectives
			general_verbs = list((soup.find("div", class_="section VERB-SECTION")).strings)[1::]
			mega_v += general_verbs
			general_adverbs = list((soup.find("div", class_="section ADVERB-SECTION")).strings)[1::]
			mega_adv += general_adverbs
			page = page + 100 # чем выше значение, тем больше страниц обработает парсер (800 - 7 страниц)
	except:
		pass	

	def clean_and_pack(*args):
		cycle = 0
		nouns = "None"
		adjectives = "None"
		verbs = "None"
		adverbs = "None"
		while cycle < 4:
			for part_of_speech in args:
				try:
					def convert_list_to_string(org_list, seperator=', '):
						return seperator.join(org_list)
					if cycle == 0:
						nouns = convert_list_to_string(part_of_speech)
					elif cycle == 1:
						adjectives = convert_list_to_string(part_of_speech)
					elif cycle == 2:
						try:
							verbs = convert_list_to_string(part_of_speech)
						except:
							pass
					elif cycle == 3:
						try:
							adverbs = convert_list_to_string(part_of_speech)
						except:
							pass
				except:
						pass
				cycle = cycle + 1
			return "NOUNS: " + nouns + "\n\nADJECTIVES: " + adjectives + "\n\nVERBS: " + verbs + "\n\nADVERBS: " + adverbs

	f = open(f'{title}.txt', "x")
	f.close()
	file = open(f'{title}.txt',"r+")
	data = title +"\n"*2 + clean_and_pack(mega_n, mega_adj,mega_v,mega_adj)

	with open(f'{title}.txt', 'r+',encoding="utf-8") as file:
		file.writelines(data)
	
	print(f"File saved as \"{title}\"")
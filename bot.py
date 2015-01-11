from bs4 import BeautifulSoup
import nltk
import requests
from itertools import chain
from random import choice
from twython import Twython, TwythonError
import os
import time

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

nltk.data.path.append('./nltk_data/')
URL = 'http://apps.timwhitlock.info/emoji/tables/unicode'
r = requests.get(URL)
soup = BeautifulSoup(r.text)

def make_emoji():
	names = soup.find_all('td', class_='name')
	clean = list(chain(*[name.contents for name in names]))
	potentials = list(chain(*[nltk.word_tokenize(name) for name in clean]))
	emoji = choice(potentials) + ' ' + choice(potentials)
	return emoji

def run():
	try:
		emoji = make_emoji()
		print emoji
		twitter.update_status(status=emoji)
		print 'zzz'
		time.sleep(3600)
	except TwythonError as e:
		print e
		pass

if __name__ == '__main__':
	while True:
		run()

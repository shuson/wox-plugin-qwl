# -*- coding: utf-8 -*-

import os
import shutil
import unicodedata
import webbrowser

import requests
from wox import Wox,WoxAPI
from bs4 import BeautifulSoup

URL = 'http://www.letscorp.net/'

def full2half(uc):
    """Convert full-width characters to half-width characters.
    """
    return unicodedata.normalize('NFKC', uc)


class Main(Wox):

    def request(self,url):
    #如果用户配置了代理，那么可以在这里设置。这里的self.proxy来自Wox封装好的对象
		if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
			proxies = {
				"http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
				"https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))
			}
			return requests.get(url,proxies = proxies)
		else:
			return requests.get(url)

    def query(self, param):
		r = self.request(URL);
		bs = BeautifulSoup(r.text, 'html.parser')
		posts = bs.find_all('a', 'title');
		result = [{
			'Title': full2half(p.contents[0]),
			'SubTitle': p.contents[0],
			'IcoPath': os.path.join('img', 'letscorp.png'),
			'JsonRPCAction': {
				'method': 'openUrl',
				'parameters': [p['href']]
			}
		} for p in posts]

		return result
	
    def openUrl(self, url):  
		webbrowser.open(url)

if __name__ == '__main__':
	Main()


from lxml import html
import requests

def downloadpage(url,path):
    page = requests.get(url)
    tree = html.fromstring(page.content)



def main():
    site = 'http://www.tzsofit.co.il/skits'
    page.requests.get(site)
    tree = html.fromstring(page.content)

if __name__ == '__main__':
    main()

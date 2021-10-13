import requests
import json
import html_to_json
from lxml import html, etree
from bs4 import BeautifulSoup

def main():
    remitly_rate = ''

    # Remitly - https://www.remitly.com/no/en
    url = 'https://www.remitly.com/us/en/india/pricing'
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')

    div_elements = soup.find_all('div', class_ = 'f1wm94yy' and 'fnsgms5')
    remitly_rate = div_elements[0].get_text()
    print (remitly_rate)

main()
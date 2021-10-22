import requests
from bs4 import BeautifulSoup
import os
from datetime import date

# Send Grid
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# Selenium
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def main():

    remitly_rate = ''
    xoom_rate = ''
    ria_rate = ''

    # Remitly - https://www.remitly.com/no/en
    url = 'https://www.remitly.com/us/en/india/pricing'
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')

    div_elements = soup.find_all('div', class_ = 'f1wm94yy' and 'fnsgms5')
    remitly_rate = '1 USD = ' + div_elements[0].get_text().replace('₹', '') + ' INR'
    print (remitly_rate)

    # Xoom - https://www.xoom.com/india/send-money
    url = 'https://www.xoom.com/india/send-money'
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')

    div_elements = soup.find_all('p', class_ = 'xvx-text-right' and 'js-ui-content-update-animation-item' and 'xvx-font-copy')
    xoom_rate = div_elements[0].get_text().replace('*', '')
    print (xoom_rate)

    # Establish chrome driver and go to site URL
    url = "https://reportdata.mytestsite.com/transactionSearch.jsp"
    driver = webdriver.Chrome(r"C:\Users\sidde\Downloads\chromedriver_win32\chromedriver.exe")
    driver.get(url)
    
    #div_elements = driver.find_elements_by_tag_name('span')
    #ria_rate = [link.get_attribute('href') for link in links]

    for elem in driver.find_elements_by_xpath('//*[@id="ria"]/div/div/div[3]/section[1]/div/div[2]/div/div/form/div[1]/p[2]/span'):
        print ("here")
        print (elem.text)

    # my_sg = sendgrid.SendGridAPIClient(api_key = 'API KEY')

    # from_email = Email("x@gmail.com")  
    # to_email = To("x@gmail.com")  
    # subject = "Remitly Exchange Rate: " + str(date.today())
    # mail_body = "Remitly Current Rate: " + remitly_rate
    # content = Content("text/plain", mail_body)

    # mail = Mail(from_email, to_email, subject, content)

    # # Get a JSON-ready representation of the Mail object
    # mail_json = mail.get()

    # # Send an HTTP POST request to /mail/send
    # HTTP_response = my_sg.client.mail.send.post(request_body=mail_json)

main()
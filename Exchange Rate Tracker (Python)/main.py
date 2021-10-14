import requests
from bs4 import BeautifulSoup
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

def main():
    remitly_rate = ''

    # Remitly - https://www.remitly.com/no/en
    url = 'https://www.remitly.com/us/en/india/pricing'
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')

    div_elements = soup.find_all('div', class_ = 'f1wm94yy' and 'fnsgms5')
    remitly_rate = div_elements[0].get_text()
    print (remitly_rate)


    my_sg = sendgrid.SendGridAPIClient(api_key = 'APIKEY')

    from_email = Email("siddesh.shewde@gmail.com")  
    to_email = To("shahaa62@gmail.com")  
    subject = "Test Email"
    content = Content("text/plain", "Test")

    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    HTTP_response = my_sg.client.mail.send.post(request_body=mail_json)

main()
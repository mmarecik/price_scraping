from price_parser import Price
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import requests
import smtplib
import json

SEC_INTERVAL = 600
GMAIL_USER = 'your_mail_address@gmail.com'
GMAIL_PASSWORD = 'your_mail_password'
SENT_TO = 'target_mail_address@gmail.com'
SUBJECT = 'Price drop noticed!'
BODY = 'Price of one of observed products has dropped.'

def send_mail(gmail_user = GMAIL_USER, password = GMAIL_PASSWORD, sent_to = SENT_TO, subject = SUBJECT, body = BODY):

    email_text = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (gmail_user, sent_to, subject, body)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(gmail_user, password)
        server.sendmail(gmail_user, sent_to, email_text)
        server.quit()

    except Exception as e:
        print('Oops! Something went wrong sending an e-mail: ', e)


def price_scraper(products_path, supported_pages_path):

    if not products_path.endswith('.json'):
        print('File with products list should be in json format')
        exit()

    if not supported_pages_path.endswith('.json'):
        print('File with list of supported pages should be in json format')
        exit()

    try:
        with open(products_path) as f_1:
            products_list = json.load(f_1)
            
        with open(supported_pages_path) as f_2:
            webpages_list = json.load(f_2)

    except Exception as e:
        print('Oops! Something went wrong while opening input files: ', e)
        exit()

    for product in products_list['products']:
        url = product['url']
        domain = url.split('/')[2]
        price = float(product['price'])

        page_included = 0
        for page in webpages_list['pages']:

            if page['page_name'] == domain:
                tag_name = page['price_tag']
                tag_class = page['tag_class']
                page_included = 1
                break

        if page_included == 0:
            response = input('Page has not been found. Want to add the %s to the list? Type Y if yes, N otherwise.\n>' % domain)

            if response == 'Y' or 'y':
                tag_name = input('Enter a html tag of %s page that contains a price of product.\n>' % domain)
                tag_class = input('Enter class of above tag.\n')
                
                webpages_list['pages'].append({
                    "page_name": domain,
                    "price_tag": tag_name,
                    "tag_class": tag_class
                })
                
                with open(supported_pages_path, 'w') as f:
                    json.dump(webpages_list, f)

            elif str.lower(response) == 'n':
                exit()

            else:
                print('Unrecognized text typed.')
                exit()

        try:
            response = requests.get(url)

        except requests.exceptions.RequestException as e:
            print(e)
            exit()

        soup = BeautifulSoup(response.text, 'lxml')
        node = soup.find(tag_name, class_=tag_class)

        if node is not None:
            price_text = node.text
            
        else:
            print("Price was not found on the website. Check if tag name and class is up-to-date.")
            continue

        actual_price = Price.fromstring(price_text)
        price_amount = actual_price.amount

        if price_amount <= price:
            msg = 'Price of a product under this address: {} has dropped to {}.'.format(url, str(price_amount))
            send_mail(body=msg)


if __name__ == "__main__":
    while True:
        price_scraper('products.json', 'supported_pages.json')
        print('{}\nProgram is sleeping. Next price checking in {} minutes.'.format(datetime.now(), float(SEC_INTERVAL) / 60))
        sleep(SEC_INTERVAL)

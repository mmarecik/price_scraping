from bs4 import BeautifulSoup
import requests
import smtplib
import json


def send_mail(gmail_user, gmail_password, sent_to, subject, body):

    sent_from = gmail_user

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, sent_to, subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, sent_to, email_text)
        server.close()

    except Exception as e:
        print("Oops! Something went wrong: ", e)


def price_scraper(products_list):

    f = open(products_list)

    data = json.load(f)

    for product in data['products']:

        url = product['url']
        price = product['price']

        print(url, "\t", price)


        # try:
        #     response = requests.get(url)
        #
        # except requests.exceptions.RequestException as e:
        #     print(e)
        #     exit()


    f.close()



    # #id status error > 500
    # soup = BeautifulSoup(response.text, 'lxml')
    #
    # price = soup.find('span', class_='product__price').text
    #
    # print(price)
    #
    # if price <= notif_price:
    #     # some action

if __name__ == "__main__":
    price_scraper('products.json')
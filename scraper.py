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
        price = product['price']


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

                tag_name = input('Enter a html tag on %s page that contains a price of product.\n>' % domain)
                tag_class = input('Enter class of above tag.\n')

                webpages_list['pages'].append({
                    "page_name": domain,
                    "price_tag": tag_name,
                    "tag_class": tag_class
                })

                with open(supported_pages_path, 'w') as f:
                    json.dump(webpages_list, f)

            elif response == 'N' or 'n':
                exit()

            else:
                print('Unrecognized text typed.')
                exit()


        try:
            response = requests.get(url)

        except requests.exceptions.RequestException as e:
            print(e)
            exit()


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
    price_scraper('products.json', 'supported_pages.json')
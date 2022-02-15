# Price scraper :money_with_wings:

This projects aims to create an interactive price monitoring program that sends notification when price of the product drops below given value :envelope:.
Prices are monitoring by checking content of specific html tags that contain price amount.


### Dependencies

This project depens on following python3 libraries:<br />
:white_check_mark: bs4<br />
:white_check_mark: requests<br />
:white_check_mark: datetime<br />
:white_check_mark: time<br />
:white_check_mark: price_parser<br />
:white_check_mark: smtplib<br />
:white_check_mark: json<br />


### Supported Websites

At the moment, the program accepts only the following websites:<br />
:white_check_mark: www.empik.com<br />
:white_check_mark: www.morele.net<br />
:white_check_mark: www.x-kom.pl<br />
:white_check_mark: www.mediamarkt.pl<br />
:white_check_mark: www.ceneo.pl<br />
:white_check_mark: https://pl.tommy.com/kobiety<br />

but you can extend the list above easily by adding new domain string and information about its html tag that contains prices of products in json file.

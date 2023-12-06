import requests
from lxml import html
import time

def main():
    bitcoin_url = "https://www.google.com/finance/quote/BTC-usd"

    bitcoin_response = requests.get(bitcoin_url)

    if bitcoin_response.status_code == 200:
        print("The Request of successful!")

        bitcoin_parsed_page = html.fromstring(bitcoin_response.content)
        bitcoin_price = bitcoin_parsed_page.xpath('//*[@class="YMlKec fxKbKc"]')

        for i in range(0,15):
            for price in bitcoin_price:
                print(price.text_content())
                time.sleep(3)

    else:
        print("That failed")


if __name__ == '__main__':
    main()

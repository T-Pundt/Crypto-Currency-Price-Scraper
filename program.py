import requests
from lxml import html
import time
import matplotlib.pyplot as plt


def main():
    bitcoin_url = "https://www.webull.com/cryptocurrency/bitcoin"
    bitcoin_price_list = []

    check = initial_check(bitcoin_url)

    if check == True:
        while True:
            pull_btc(bitcoin_url, bitcoin_price_list)
            # PlaceHolder to add more Currencies
            display_graph(bitcoin_price_list)
            time.sleep(4)
    else:
        print("RIP")


def pull_btc(url, price_list):  # rework this function so its universal for all the different currencies
    bitcoin_response = requests.get(url)
    bitcoin_parsed_page = html.fromstring(bitcoin_response.content)
    bitcoin_price = bitcoin_parsed_page.xpath('//*[@class="price"]')
    for price in bitcoin_price:
        print(price.text_content())
        price_string = str(price.text_content())
        price_list.append(price_string)


def display_graph(btc_list):
    x_values = range(1, len(btc_list) + 1)
    plt.plot(x_values, btc_list, label="Bitcoin")

    plt.legend()
    plt.show()


def initial_check(btc_url) -> bool:
    bitcoin_response = requests.get(btc_url)
    if bitcoin_response.status_code == 200:
        print("The Request of successful!")
        return True
    else:
        return False


if __name__ == '__main__':
    main()

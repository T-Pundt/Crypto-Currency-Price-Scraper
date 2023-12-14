import requests
from lxml import html
import time
import matplotlib.pyplot as plt
import datetime


def main():
    bitcoin_url = "https://www.webull.com/cryptocurrency/bitcoin"
    bitcoin_price_list = []
    eth_url = "https://www.webull.com/cryptocurrency/ethereum"
    eth_price_list = []
    ltc_url = "https://www.webull.com/cryptocurrency/litecoin"
    ltc_price_list = []

    time_of_price = []

    btc_check = initial_check(bitcoin_url)
    eth_check = initial_check(eth_url)
    ltc_check = initial_check(ltc_url)

    if btc_check and eth_check and ltc_check:
        while True:
            pull_crypto(bitcoin_url, bitcoin_price_list)
            pull_crypto(eth_url, eth_price_list)
            pull_crypto(ltc_url, ltc_price_list)

            log_current_time(time_of_price)
            display_graph(bitcoin_price_list, eth_price_list, ltc_price_list)
            time.sleep(4)
    else:
        print("RIP")


def pull_crypto(url, price_list):
    response = requests.get(url)
    parsed_page = html.fromstring(response.content)
    price = parsed_page.xpath('//*[@class="price"]')

    for item in price:
        print(item.text_content())
        item_string = str(item.text_content())
        price_list.append(item_string)


def display_graph(btc_list, eth_list, lsc_list):
    x_values = range(1, len(btc_list) + 1)
    plt.plot(x_values, btc_list, label="Bitcoin")

    plt.legend()
    plt.show()


def initial_check(url) -> bool:
    response = requests.get(url)
    if response.status_code == 200:
        print("The Request of successful!")
        return True
    else:
        return False


def log_current_time(time_list):
    current_time = datetime.datetime.now()

    hour = current_time.strftime("%H")
    minute = current_time.strftime("%M")
    second = current_time.strftime("%S")

    current_time = hour + ":" + minute + ":" + second

    print(current_time)



if __name__ == '__main__':
    main()

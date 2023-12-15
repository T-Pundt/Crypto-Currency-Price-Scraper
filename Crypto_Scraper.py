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
            time.sleep(10)
    else:
        print("The request for HTML was denied")


def pull_crypto(url, price_list):
    response = requests.get(url)
    if response.status_code != 200:
        print("HTML request denied")
        exit()

    parsed_page = html.fromstring(response.content)
    price = parsed_page.xpath('//*[@class="price"]')

    for item in price:
        print(item.text_content())
        item_string = str(item.text_content())
        item_float = item_string.replace(",", "")
        item_float = float(item_float)
        price_list.append(item_float)


def display_graph(btc_list, eth_list, ltc_list):
    plt.style.use("dark_background")

    x_values = range(1, len(btc_list) + 1)

    plt.subplot(1, 3, 1)
    plt.plot(x_values, ltc_list, color="blue")
    plt.title("Litecoin")
    bot = min(ltc_list) - .1
    top = max(ltc_list) + .1
    plt.ylim(bot, top)
    plt.xticks([])

    plt.subplot(1, 3, 2)
    plt.plot(x_values, eth_list, color="green")
    plt.title("Ethereum")
    bot = min(eth_list) - 1
    top = max(eth_list) + 1
    plt.ylim(bot, top)
    plt.xticks([])

    plt.subplot(1, 3, 3)
    plt.plot(x_values, btc_list, color="orange")
    plt.title("Bitcoin")
    bot = min(btc_list) - 5
    top = max(btc_list) + 5
    plt.ylim(bot, top)
    plt.xticks([])

    plt.subplots_adjust(wspace=1)
    plt.show()

    print(ltc_list)
    print(eth_list)
    print(btc_list)


def initial_check(url) -> bool:
    response = requests.get(url)
    if response.status_code == 200:
        print("The Request of successful!")
        return True
    else:
        print(response.status_code)
        return False


def log_current_time(time_list):
    current_time = datetime.datetime.now()

    hour = current_time.strftime("%H")
    minute = current_time.strftime("%M")
    second = current_time.strftime("%S")

    current_time = hour + ":" + minute + ":" + second

    time_list.append(current_time)


if __name__ == '__main__':
    main()

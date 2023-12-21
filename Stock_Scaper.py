import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import matplotlib.pyplot as plt
import datetime


def main():
    bitcoin_price_list, eth_price_list, ltc_price_list, time_of_price = [], [], [], []
    bitcoin_url = "https://www.webull.com/quote/nasdaq-tsla"
    eth_url = "https://www.webull.com/quote/nasdaq-tsla"
    ltc_url = "https://www.webull.com/quote/nasdaq-tsla"

    btc_check = initial_check(bitcoin_url)
    eth_check = initial_check(eth_url)
    ltc_check = initial_check(ltc_url)

    if btc_check and eth_check and ltc_check:
        try:
            while True:
                pull_stock(bitcoin_url, bitcoin_price_list)
                pull_stock(eth_url, eth_price_list)
                pull_stock(ltc_url, ltc_price_list)

                log_current_time(time_of_price)
                display_graph(bitcoin_price_list, eth_price_list, ltc_price_list)
                time.sleep(10)
        except KeyboardInterrupt:
            # Call the function that exports the data to an Excel sheet
            print("Program was ended by the user")
    else:
        print("The request for HTML was denied")


def pull_stock(url, price_list):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    price_element = soup.find('div', class_='csr121 csr118')
    if price_element:
        price = price_element.text.strip()
        print(f"The price is now {price}")
        price = float(price)
        price_list.append(price)


def display_graph(btc_list, eth_list, ltc_list):
    plt.style.use("dark_background")

    x_values = range(1, len(btc_list) + 1)

    plt.subplot(1, 3, 1)
    plt.plot(x_values, ltc_list, color="blue")
    plt.title("Litecoin")
    bot = min(ltc_list) - 1
    top = max(ltc_list) + 1
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
    bot = min(btc_list) - 1
    top = max(btc_list) + 1
    plt.ylim(bot, top)
    plt.xticks([])

    plt.subplots_adjust(wspace=1)
    plt.pause(.1)


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

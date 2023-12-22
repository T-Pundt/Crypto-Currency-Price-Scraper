import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import matplotlib.pyplot as plt
import datetime
from openpyxl import Workbook


def main():
    tesla_price_list, apple_price_list, amazon_price_list = [], [], []
    tesla_time_list, apple_time_list, amazon_time_list = [], [], []
    tesla_url = "https://www.webull.com/quote/nasdaq-tsla"
    apple_url = "https://www.webull.com/quote/nasdaq-aapl"
    amazon_url = "https://www.webull.com/quote/nasdaq-amzn"
    tesla_check = initial_check(tesla_url)
    apple_check = initial_check(apple_url)
    amazon_check = initial_check(amazon_url)

    loop_amount = input("How many rows of data would you like to collect?: ")
    loop_amount = int(loop_amount)

    if tesla_check and apple_check and amazon_check:
        for i in range(1, loop_amount + 1):
            pull_stock(tesla_url, tesla_price_list)
            log_current_time(tesla_time_list)

            pull_stock(apple_url, apple_price_list)
            log_current_time(apple_time_list)

            pull_stock(amazon_url, amazon_price_list)
            log_current_time(amazon_time_list)

            display_graph(tesla_price_list, apple_price_list, amazon_price_list)
            time.sleep(10)
            print(f"Completed {i} rows")

    else:
        print("The request for HTML was denied")
        exit()

    export_data_to_excel(tesla_price_list, apple_price_list, amazon_price_list, tesla_time_list, apple_time_list, amazon_time_list)
    print("Program was ended by the user")
    exit()


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
        price = float(price)
        price_list.append(price)
    else:
        price_element = soup.find('div', class_='csr122 csr118')
        price = price_element.text.strip()
        price = float(price)
        price_list.append(price)

    driver.quit()


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


def export_data_to_excel(tesla_price, apple_price, amazon_price, tesla_time, apple_time, amazon_time):
    data_columns = [tesla_price, apple_price, amazon_price, tesla_time, apple_time, amazon_time]

    data_rows = zip(*data_columns)

    workbook = Workbook()
    sheet = workbook.active

    headers = "Tesla Price", "Apple Price", "Amazon Price", "Tesla Time", "Apple Time", "Amazon Time"
    sheet.append(headers)

    for row in data_rows:
        sheet.append(row)

    excel_filename = "output_data.xlsx"
    workbook.save(excel_filename)


if __name__ == '__main__':
    main()

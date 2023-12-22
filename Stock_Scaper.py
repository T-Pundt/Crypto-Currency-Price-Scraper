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
    loop_amount = ""
    tesla_url = "https://www.webull.com/quote/nasdaq-tsla"
    apple_url = "https://www.webull.com/quote/nasdaq-aapl"              # initialize variables used in the program
    amazon_url = "https://www.webull.com/quote/nasdaq-amzn"
    tesla_check = initial_check(tesla_url)
    apple_check = initial_check(apple_url)
    amazon_check = initial_check(amazon_url)

    # prompt the user to enter the amount of data they want to pull
    user_input = input("How many rows of data would you like to collect?: ")

    # iterates over the user input and only stores the digits that were entered
    for char in user_input:
        if char.isdigit():
            loop_amount += char

    # changes the data type of loop amount to int
    loop_amount = int(loop_amount)

    # preforms the loop if there is an ability to access the html page, otherwise exit the program
    if tesla_check and apple_check and amazon_check:
        for i in range(1, loop_amount + 1):
            pull_stock(tesla_url, tesla_price_list)
            log_current_time(tesla_time_list)

            pull_stock(apple_url, apple_price_list)
            log_current_time(apple_time_list)

            pull_stock(amazon_url, amazon_price_list)
            log_current_time(amazon_time_list)

            display_graph(tesla_price_list, apple_price_list, amazon_price_list)
            print(f"Completed {i} rows")
            time.sleep(10)

    else:
        print("The request for HTML was denied")
        exit()

    # once the loop is done executing export the data to an Excel sheet
    export_data_to_excel(tesla_price_list, apple_price_list, amazon_price_list,
                         tesla_time_list, apple_time_list, amazon_time_list)

    print("Program completed successfully")
    exit()


def pull_stock(url, price_list):
    chrome_options = Options()
    chrome_options.add_argument("--headless")                           # prevents the browser from popping up

    driver = webdriver.Chrome(options=chrome_options)                   # adds the options specified above
    driver.get(url)
    page_source = driver.page_source

    page = BeautifulSoup(page_source, 'html.parser')            # parses the html page

    price_element = page.find('div', class_='csr121 csr118')      # searches page for the class containing price
    if price_element:
        price = price_element.text.strip()
        price = float(price)                                           # The webpage has two main classes for displaying
        price_list.append(price)                                        # Price if the first class is empty the second
    else:                                                                # class is searched and the data is stored
        price_element = page.find('div', class_='csr122 csr118')     # respectively
        price = price_element.text.strip()
        price = float(price)
        price_list.append(price)

    driver.quit()


def display_graph(tesla_list, apple_list, amazon_list):
    plt.style.use("dark_background")                                    # switch to dark mode

    x_values = range(1, len(tesla_list) + 1)

    plt.subplot(1, 3, 1)                                         # this block of code changes graph placement
    plt.plot(x_values, amazon_list, color="blue")                # values and line color
    plt.title("Amazon")                                                # title of graph
    bot = min(amazon_list) - 1                                         # y min
    top = max(amazon_list) + 1                                         # y max
    plt.ylim(bot, top)                                           # sets y min and max
    plt.xticks([])                                                     # hides the x values

    plt.subplot(1, 3, 2)
    plt.plot(x_values, apple_list, color="green")
    plt.title("Apple")
    bot = min(apple_list) - 1
    top = max(apple_list) + 1
    plt.ylim(bot, top)
    plt.xticks([])

    plt.subplot(1, 3, 3)
    plt.plot(x_values, tesla_list, color="orange")
    plt.title("Tesla")
    bot = min(tesla_list) - 1
    top = max(tesla_list) + 1
    plt.ylim(bot, top)
    plt.xticks([])

    plt.subplots_adjust(wspace=1)                                       # adjusts the width
    plt.pause(.1)                                                       # displays the graph


def initial_check(url) -> bool:
    response = requests.get(url)
    if response.status_code == 200:                                     # if the html page is able to accessed
        return True                                                     # return true, otherwise return false
    else:
        print(response.status_code)
        return False


def log_current_time(time_list):
    current_time = datetime.datetime.now()                              # finds the current time and stores it

    hour = current_time.strftime("%H")                                  # grabs the hours
    minute = current_time.strftime("%M")                                # grabs the minutes
    second = current_time.strftime("%S")                                # grabs the seconds

    current_time = hour + ":" + minute + ":" + second                   # creates a variable with time elements

    time_list.append(current_time)                                      # appends the time list provided with time


def export_data_to_excel(tesla_price, apple_price, amazon_price, tesla_time, apple_time, amazon_time):
    data_columns = [tesla_price, apple_price, amazon_price, tesla_time, apple_time, amazon_time]

    data_rows = zip(*data_columns)                                      # organizes data for Excel sheet

    workbook = Workbook()                                               # creates a new excel file
    sheet = workbook.active                                             # selects the sheet for data entry

    # specifies headers and adds them to the Excel sheet
    headers = "Tesla Price", "Apple Price", "Amazon Price", "Tesla Time", "Apple Time", "Amazon Time"
    sheet.append(headers)

    for row in data_rows:
        sheet.append(row)                                               # adds the data according to their rows

    workbook.save("Sock_Prices.xlsx")                                   # saves the Excel sheet


if __name__ == '__main__':
    main()

import requests
from lxml import html


def main():
    bitcoin_url = "https://www.coindesk.com/price/bitcoin/"

    bitcoin_response = requests.get(bitcoin_url)

    if bitcoin_response.status_code == 200:
        print("The Request of successful!")
    else:
        print("That failed")


if __name__ == '__main__':
    main()

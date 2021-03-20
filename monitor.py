from bs4 import BeautifulSoup
import requests, termcolor, re, time
from pygame import mixer
from classes.classes import Stock

firefox_header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}
priceArr = []
stock_arr = []


def playSound():
    mixer.init()
    mixer.music.load('./audio_files/Cash_Register_Sound_Effect.mp3')
    mixer.music.play()
    time.sleep(5)


def addValues():
    urlsDoc = open("urls.txt")
    for line in urlsDoc:
        if line == "\n" or line.startswith("#"):
            continue

        lineSplit = line.split("=")

        # Format: Name=URL{=Target_Price} where {...} is optional
        name = lineSplit[0]
        url = lineSplit[1].replace("\\n", '')

        stock = Stock(name, url, None)

        # If a target price was set, check for it
        if len(lineSplit) > 2:
            target_price = float(lineSplit[2])
            stock.target_price = target_price

        stock_arr.append(stock)


def checkStock(starting):
    for stock in stock_arr:
        print(stock.name, end="\t")

        try:
            page = requests.get(stock.url, headers=firefox_header)
            pageSoup = BeautifulSoup(page.content, 'html.parser')

            classFind = str(pageSoup.find(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"))
            # print(classFind)
            nums = re.findall(r'\d+\.\d+', classFind)
            if nums is None or len(nums) < 2:
                continue
            # [0] gives the 0.3s from the class name instead of value
            price = float(nums[1])

            if not starting:
                prev = stock.price_curr
                text = ""
                # Current price logic
                if price > prev:
                    text = termcolor.colored(str(price), 'green')
                elif price < prev:
                    text = termcolor.colored(str(price), 'red')
                else:
                    text = termcolor.colored(str(price), 'white')
                print(text, end="\t")
                stock.price_curr = price
                # High price logic
                if price > stock.price_high:
                    text = termcolor.colored("HIGH\t" + str(price), 'green')
                    print(text, end="\t")
                    stock.price_high = price
                else:
                    text = termcolor.colored(str(stock.price_high), 'blue')
                    print("HIGH", text, end="\t")
                # Low price logic
                if price < stock.price_low:
                    text = termcolor.colored("LOW " + str(price), 'red')
                    print(text)
                    stock.price_low = price
                else:
                    text = termcolor.colored(str(stock.price_low), 'yellow')
                    print("LOW", text)
                # Check target price
                if stock.target_price:
                    if price >= stock.target_price:
                        playSound()
            else:
                stock.price_curr = price
                stock.price_high = price
                stock.price_low = price
                print(price)
        except:
            print("ERROR FETCHING. CONTINUING.")

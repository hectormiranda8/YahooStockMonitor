from bs4 import BeautifulSoup
import requests, termcolor, re, time
from pygame import mixer

firefox_header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}
priceArr = []


def playSound():
    mixer.init()
    mixer.music.load('./audio_files/Cash_Register_Sound_Effect.mp3')
    mixer.music.play()
    time.sleep(5)


def checkValue():
    urlsDoc = open("urls.txt")
    lineCount = 0

    for line in urlsDoc:
        if line.startswith("#"):
            continue

        lineSplit = line.split("=")

        name = lineSplit[0]
        url = lineSplit[1].replace("\\n", '')

        # print(lineSplit)
        print(name, end=" ")
        # print(url)

        page = requests.get(url, headers=firefox_header)
        pageSoup = BeautifulSoup(page.content, 'html.parser')
        # print(pageSoup)

        classFind = str(pageSoup.find(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"))
        # print(classFind)
        # [0] gives the 0.3s from the class name instead of value
        nums = re.findall(r'\d+\.\d+', classFind)
        if nums is None or len(nums) < 2:
            continue
        price = float(nums[1])
        # print(str(price) + "\n")

        if lineCount < len(priceArr):
            prev = priceArr[lineCount]
            text = ""
            if price >= prev:
                text = termcolor.colored(str(price), 'green')
            else:
                text = termcolor.colored(str(price), 'red')
            priceArr[lineCount] = price
            print(text)
        else:
            priceArr.append(price)
            print(str(price))

        # print(priceArr)

        # If a target price was set, check for it
        if len(lineSplit) > 2:
            priceTarget = float(lineSplit[2])
            if price >= priceTarget:
                playSound()

        lineCount += 1

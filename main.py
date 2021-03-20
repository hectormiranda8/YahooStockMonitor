import monitor, time, os

starting = True


def main():
    global starting

    print("Starting script. CTRL-C to EXIT.")

    try:
        while True:
            if starting:
                monitor.addValues()
                monitor.checkStock(starting)
                starting = False
                continue
            monitor.checkStock(starting)
            time.sleep(1)
    except:
        os.system("python main.py")


main()

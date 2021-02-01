import monitor, time


def main():
    while True:
        monitor.checkValue()
        time.sleep(1)
    # monitor.checkValue()


main()

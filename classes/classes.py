class Stock:
    def __init__(self, name, url, target_price):
        if len(name) <= 3:
            self.name = name + " "
        else:
            self.name = name
        self.url = url
        self.target_price = target_price
        self.price_curr = 0
        self.price_high = 0
        self.price_low = 0

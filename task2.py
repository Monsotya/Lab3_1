import json
import os
from datetime import datetime


class Pizza:
    """Class describes base class for pizza"""
    __basic = 40

    def __init__(self, *args):
        with open("toppings.json", "r") as read_file:
            data = json.load(read_file)
        self.__toppings = []
        self.__cost = Pizza.__basic
        toppings = args[0]
        for ingredient in toppings:
            if not (ingredient in data):
                raise ValueError
            self.__cost += data.get(ingredient)
            self.__toppings.append(ingredient)

    @property
    def cost(self):
        return self.__cost

    @property
    def toppings(self):
        return self.__toppings


class Monday_Pizza(Pizza):
    def __init__(self, *args):
        toppings = ["tomato", "bacon", "basil", "chili", "mozzarella"]
        for i in args:
            toppings += i
        super().__init__(toppings)


class Tuesday_Pizza(Pizza):
    def __init__(self, *args):
        toppings = ["mushroom", "pineapple", "chicken", "corn", "mozzarella"]
        for i in args:
            toppings += i
        super().__init__(toppings)


class Wednesday_Pizza(Pizza):
    def __init__(self, *args):
        toppings = ["onion", "ham", "basil", "chili", "mozzarella"]
        for i in args:
            toppings += i
        super().__init__(toppings)


class Thursday_Pizza(Pizza):
    def __init__(self, *args):
        toppings = ["olives", "prosciutto", "basil", "chilli", "cheddar"]
        for i in args:
            toppings += i

        super().__init__(toppings)


class Friday_Pizza(Pizza):
    def __init__(self, *args):
        toppings = ["tomato", "pepperoni", "olives", "mozzarella"]
        for i in args:
            toppings += i
        super().__init__(toppings)


class Saturday_Pizza(Pizza):
    def __init__(self, *args):
        toppings = ["mushroom", "olives", "chicken", "cheddar", "corn"]
        for i in args:
            toppings += i
        super().__init__(toppings)


class Sunday_Pizza(Pizza):
    def __init__(self, *args):
        toppings = ["pineapple", "ham", "corn", "prosciutto", "cheddar"]
        for i in args:
            toppings += i

        super().__init__(toppings)


class Order_Pizza:
    """Creates an order depending on day"""
    __order_number = 0
    def __init__(self, *args):
        __order_number = 0
        week_day = datetime.today().weekday()
        if not week_day:
            self.__pizza = Monday_Pizza(args)
        elif week_day == 1:
            self.__pizza = Tuesday_Pizza(args)
        elif week_day == 2:
            self.__pizza = Wednesday_Pizza(args)
        elif week_day == 3:
            self.__pizza = Thursday_Pizza(args)
        elif week_day == 4:
            self.__pizza = Friday_Pizza(args)
        elif week_day == 5:
            self.__pizza = Saturday_Pizza(args)
        else:
            self.__pizza = Sunday_Pizza(args)

        self.__cost = self.__pizza.cost
        self.__toppings = self.__pizza.toppings
        self.save_ticket()

    def save_ticket(self):
        """Adds order to JSON file"""
        order_properties = dict([("cost", self.__cost), ("toppings", str(self.__toppings))])
        current_order = dict([(str(Order_Pizza.__order_number), order_properties)])

        with open("order.json", "r") as infile:
            if os.stat("order.json").st_size != 0:
                orders = json.load(infile)
                orders.update(current_order)
            else:
                orders = current_order

        with open('order.json', 'w') as outfile:
            json.dump(orders, outfile, indent=4)

    def __str__(self):
        return f'This is {type(self.__pizza).__name__}\nPrice: {self.__cost} grn\nToppings: {self.__toppings}'


obj = Order_Pizza("mushroom", "pineapple")
print(obj)
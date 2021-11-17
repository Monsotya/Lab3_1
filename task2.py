import json
import os
from datetime import datetime


class Pizza:
    """Class describes base class for pizza"""
    __base_for_pizza = 40

    def __init__(self, *args):
        with open("toppings.json", "r") as read_file:
            data = json.load(read_file)
        self.__toppings = []
        self.__cost = Pizza.__base_for_pizza
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


class MondayPizza(Pizza):
    def __init__(self, *args):
        toppings = ["tomato", "bacon", "basil", "chilli", "mozzarella"]
        for i in args:
            toppings += i
        super().__init__(toppings)


class TuesdayPizza(Pizza):
    def __init__(self, *args):
        toppings = ["mushroom", "pineapple", "chicken", "corn", "mozzarella"]
        for i in args:
            toppings += i
        super().__init__(toppings)


class WednesdayPizza(Pizza):
    def __init__(self, *args):
        toppings = ["onion", "ham", "basil", "chilli", "mozzarella"]
        for i in args:
            toppings += i
        super().__init__(toppings)


class ThursdayPizza(Pizza):
    def __init__(self, *args):
        toppings = ["olives", "prosciutto", "basil", "chilli", "cheddar"]
        for i in args:
            toppings += i

        super().__init__(toppings)


class FridayPizza(Pizza):
    def __init__(self, *args):
        toppings = ["tomato", "pepperoni", "olives", "mozzarella"]
        for i in args:
            toppings += i
        super().__init__(toppings)


class SaturdayPizza(Pizza):
    def __init__(self, *args):
        toppings = ["mushroom", "olives", "chicken", "cheddar", "corn"]
        for i in args:
            toppings += i
        super().__init__(toppings)


class SundayPizza(Pizza):
    def __init__(self, *args):
        toppings = ["pineapple", "ham", "corn", "prosciutto", "cheddar"]
        for i in args:
            toppings += i

        super().__init__(toppings)


class OrderPizza:
    """Creates an order depending on day"""
    __order_number = 0
    __pizza_dictionary = {0: MondayPizza, 1: TuesdayPizza, 2: WednesdayPizza, 3: ThursdayPizza,
                          4: FridayPizza, 5: SaturdayPizza, 6: SundayPizza}

    def __init__(self, *args):
        __order_number = 0
        week_day = datetime.today().weekday()
        self.__pizza = OrderPizza.__pizza_dictionary.get(week_day)(args)
        self.__cost = self.__pizza.cost
        self.__toppings = self.__pizza.toppings
        self.save_ticket()

    def save_ticket(self):
        """Adds order to JSON file"""
        order_properties = dict([("cost", self.__cost), ("toppings", str(self.__toppings))])
        current_order = dict([(str(OrderPizza.__order_number), order_properties)])

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


obj = OrderPizza("mushroom", "pineapple")
print(obj)

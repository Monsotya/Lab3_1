import json
import os
from datetime import datetime

LATE_TICKET_TIME = 10
ADVANCED_TICKET_TIME = 60


class Event:
    """Describes an event
                Contains:
                    date(datetime),
                    code(str),
                    price(double),
                    description(str),
                    total_quantity(int),
                    left_tickets(int) """

    def __init__(self, event):
        with open("BD.json", "r") as read_file:
            data = json.load(read_file)
        if not (event in data):
            raise ValueError

        self.__code = event
        self.__price = data.get(event).get("price")
        self.__description = data.get(event).get("description")
        self.__date = datetime.strptime(data.get(event).get("date"), "%Y-%m-%d %H:%M")
        self.__total_quantity = data.get(event).get("quantity")
        self.__left_tickets = self.__total_quantity

    def order_ticket(self, is_student):
        if self.__left_tickets == 0:
            raise ValueError
        if not isinstance(is_student, bool):
            raise TypeError

        self.__left_tickets -= 1
        today = datetime.now()
        if is_student:
            return StudentTicket(self)
        elif (self.__date - today).days < LATE_TICKET_TIME:
            return LateTicket(self)
        elif (self.__date - today).days >= ADVANCED_TICKET_TIME:
            return AdvancedTicket(self)
        else:
            return RegularTicket(self, self.__price)

    @property
    def price(self):
        return self.__price

    @property
    def code(self):
        return self.__code

    @property
    def description(self):
        return self.__description

    @property
    def date(self):
        return self.__date

    @property
    def total_quantity(self):
        return self.__total_quantity

    @property
    def left_tickets(self):
        return self.__left_tickets

    @left_tickets.setter
    def left_tickets(self, number):
        if not isinstance(number, int):
            raise TypeError

        self.__left_tickets = number


class RegularTicket:
    """Base class for a ticket"""

    def __init__(self, event, price):
        self.__ticket_number = event.code + "_" + str(event.total_quantity - event.left_tickets)
        self.__price = price
        self.__event = event
        self.save_ticket()

    def get_info(self, ticket_number):

        """Returns information about ticket"""
        with open("BD.json", "r") as read_file:
            data = json.load(read_file)
        with open("data.json", "r") as infile:
            if os.stat("data.json").st_size != 0:
                tickets = json.load(infile)
                if ticket_number in tickets:
                    return data.get(ticket_number)
                else:
                    raise ValueError
            else:
                raise ValueError

    @property
    def price(self):
        return self.__price

    def save_ticket(self):
        """Adds ticket to JSON file"""

        current_ticket = dict([(self.__ticket_number, self.__price)])

        with open("data.json", "r") as infile:
            if os.stat("data.json").st_size != 0:
                tickets = json.load(infile)
                tickets.update(current_ticket)
            else:
                tickets = current_ticket

        with open('data.json', 'w') as outfile:
            json.dump(tickets, outfile, indent=4)

    def __str__(self):
        return f'Ticket`s number: {self.__ticket_number}\nThis is {type(self).__name__}\n' \
               f'Price: {self.__price}\nDescription: {self.__event.description}\nDate: {self.__event.date}'


class AdvancedTicket(RegularTicket):
    def __init__(self, event):
        self.__price = event.price * 0.6
        super().__init__(event, self.__price)


class StudentTicket(RegularTicket):
    def __init__(self, event):
        self.__price = event.price * 0.5
        super().__init__(event, self.__price)


class LateTicket(RegularTicket):
    def __init__(self, event):
        self.__price = event.price * 1.1
        super().__init__(event, self.__price)


print("Enter event`s id")
id_event = input()
event = Event(id_event)
print("Are you a student?(yes/no)")
answer = input()
if answer == "yes":
    ticket = event.order_ticket(True)
    print(ticket)
else:
    ticket = event.order_ticket(False)
    print(ticket)

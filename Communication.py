import socket
import re

class Communication:
    
    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("",5005))
        self.address = address

    def send(self, order):
        self.sock.sendto(order.toString().encode("ascii"), self.address)


class Order:
    def __init__(self, feedcode, action, price, volume):
        self.type = "ORDER"
        self.username = "Mr_Complex"
        self.feedcode = feedcode
        self.action = action
        self.price = price
        self.volume = volume
    
    def toString(self):
        return "TYPE=" + str(self.type) + "|USERNAME=" + str(self.username) + "|FEEDCODE=" + str(self.feedcode) + "|ACTION=" + str(self.action) + "|PRICE=" + str(self.price) + "|VOLUME=" + str(self.volume)
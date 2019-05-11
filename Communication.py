import socket
import re

class Communication:
    
    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("test1")
        self.sock.bind(("",8000))
        print("test1")
        self.address = address
        print("test1")
        #self.sock.sendto("TYPE=SUBSCRIPTION_REQUEST".encode("ascii"),self.address)

    def send(self, order):
        self.sock.sendto(order.toString().encode("ascii"),address)


class Order:
    def __init__(self, feedcode, action, price, volume):
        self.type = "ORDER"
        self.username = ""
        self.feedcode = feedcode
        self.action = action
        self.price = price
        self.volume = volume
    
    def toString(self):
        return "TYPE=" + str(self.type) + "|USERNAME=" + str(self.username) + "|FEEDCODE=" + str(self.feedcode) + "|ACTION=" + str(self.action) + "|PRICE=" + str(self.price) + "|VOLUME=" + str(self.volume)
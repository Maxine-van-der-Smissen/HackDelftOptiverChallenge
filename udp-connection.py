import socket
import re
from Communication import *

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address=("188.166.115.7",7001)
sock.bind(("",5000))
sock.sendto("TYPE=SUBSCRIPTION_REQUEST".encode("ascii"),address)

sender = Communication(("188.166.115.7",8001))

while True:
    data,addr = sock.recvfrom(1024)
    data = data.decode('utf-8')

    # Find out if it is a price or a Trade
    if data.find("TYPE=TRADE")==0:
        # Trade is shorter 5
        fields = data.split('|')
        feedcode = fields[1]
        side = fields[2]
        ask_price = float(re.search(r'\d+', fields[3]).group())
        ask_volume = int(re.search(r'\d+', fields[4]).group())

        # print(price)
    elif data.find("TYPE=PRICE")==0:
         # Trade is shorter 5
        fields = data.split('|')
        feedcode = fields[1]
        bid_price = float(re.search(r'\d+', fields[2]).group())
        bid_volume = int(re.search(r'\d+', fields[3]).group())
        ask_price = float(re.search(r'\d+', fields[4]).group())
        ask_volume = int(re.search(r'\d+', fields[5]).group())


        print(bid_price)

        if bid_price >= 3090:
            sender.send(Order(feedcode, "SELL", bid_price, 1))
            print("Order Send!")

        elif ask_price <= 3070:
            sender.send(Order(feedcode, "BUY", ask_price, 1))
            print("Order Send!")
    
    print("test1")
    recieveData,a = sender.sock.recvfrom(1024)
    print("test2")
    recieveData = recieveData.decode('utf-8')
    print("test3")

    if recieveData.find("TYPE=ORDER_ACK")==-1:
        print("Order Acknowledged!!!")
        fields = recieveData.split('|')
        print(fields[len(fields)-1])


    

import socket
import re
from Communication import *

sock_iml = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address_iml=("188.166.115.7",7001)
sock_iml.bind(("",5000))
sock_iml.sendto("TYPE=SUBSCRIPTION_REQUEST".encode("ascii"),address_iml)

# sock_eml = Communication(("188.166.115.7",8001))

sock_eml = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address_eml=("188.166.115.7",8001)
sock_eml.bind(("",5005))
# sock_eml.sendto("TYPE=SUBSCRIPTION_REQUEST".encode("ascii"),address_eml)

# sender = Communication(("188.166.115.7",8001))

while True:
    data,addr = sock_iml.recvfrom(1024)
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
            sock_eml.sendto(Order(feedcode, "SELL", bid_price, 1).toString().encode("ascii"),address_eml)
           
            print("Order Send!")
            recieveData,a = sock_eml.recvfrom(1024)
            recieveData = recieveData.decode('utf-8')

            if recieveData.find("TYPE=ORDER_ACK")==0:
                print("Order Acknowledged!!!")
                fields = recieveData.split('|')
                print(fields[len(fields)-1])

        elif ask_price <= 3070:
            sock_eml.sendto(Order(feedcode, "BUY", ask_price, 1).toString().encode("ascii"),address_eml)
     
            print("Order Send!")
            recieveData,a = sock_eml.recvfrom(1024)
            recieveData = recieveData.decode('utf-8')
    
            if recieveData.find("TYPE=ORDER_ACK")==0:
                print("Order Acknowledged!!!")
                fields = recieveData.split('|')
                print(fields[len(fields)-1])

   


    

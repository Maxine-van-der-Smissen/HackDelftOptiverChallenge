import socket
import re
from Communication import *

sock_iml = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address_iml=("188.166.115.7",7001)
sock_iml.bind(("",5000))
sock_iml.sendto("TYPE=SUBSCRIPTION_REQUEST".encode("ascii"),address_iml)


address_eml=("188.166.115.7",8001)
sock_eml = Communication(address_eml)

#sock_eml.bind(("",5005))


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
        feedcode = fields[1][9:]
        bid_price = float(re.search(r'\d+', fields[2]).group())
        bid_volume = int(re.search(r'\d+', fields[3]).group())
        ask_price = float(re.search(r'\d+', fields[4]).group())
        ask_volume = int(re.search(r'\d+', fields[5]).group())


        print(bid_price)

        """ if feedcode == "ESX-FUTURE" and bid_price >= 3000:
            order = Order(feedcode, "SELL", bid_price, 1)
            sock_eml.send(order)
           
            print(order.toString())
            recieveData,a = sock_eml.sock.recvfrom(1024)
            recieveData = recieveData.decode('utf-8')

            if recieveData.find("TYPE=ORDER_ACK")==0:
                print("Order Acknowledged!!!")
                print(recieveData)
                fields = recieveData.split('|')
                print(fields[len(fields)-1])
            

        elif feedcode == "ESX-FUTURE" and ask_price <= 3120:
            order = Order(feedcode, "BUY", ask_price+5, 1)
            sock_eml.send(order)
     
            print(order.toString())
            recieveData,a = sock_eml.sock.recvfrom(1024)
            recieveData = recieveData.decode('utf-8')
    
            if recieveData.find("TYPE=ORDER_ACK")==0:
                print("Order Acknowledged!!!")
                print(recieveData)
                fields = recieveData.split('|')
                print(fields[len(fields)-1]) """

   


    

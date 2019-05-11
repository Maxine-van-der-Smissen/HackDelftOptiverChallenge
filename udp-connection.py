import socket
import re

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address=("188.166.115.7",7001)
sock.bind(("",5000))
sock.sendto("TYPE=SUBSCRIPTION_REQUEST".encode("ascii"),address)


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
    

    

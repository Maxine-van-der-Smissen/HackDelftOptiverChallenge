import socket
import re
import csv
import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address=("188.166.115.7",7001)
sock.bind(("",5000))
sock.sendto("TYPE=SUBSCRIPTION_REQUEST".encode("ascii"),address)
records = 0

with open('prices_' + datetime.datetime.now().strftime('%H_%M_%S') + '.csv', mode='w', newline='') as prices:
    with open('trades_' + datetime.datetime.now().strftime('%H_%M_%S') + '.csv', mode='w', newline='') as trades:
        prices_writer = csv.writer(prices, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        trades_writer = csv.writer(trades, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        prices_writer.writerow(['Timestamp', 'Instrument', 'Bid Price', 'Bid Volume', 'Ask Price', 'Ask Volume'])
        trades_writer.writerow(['Timestamp', 'Traded Instrument', 'Traded Side', 'Traded Price', 'Traded Volume'])

        while True:
            data,addr = sock.recvfrom(1024)
            data = data.decode('utf-8')
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')

            if data.find("TYPE=PRICE")==0:
                fields = data.split('|')
                feedcode = fields[1][9:]
                bid_price = float(re.search(r'\d+', fields[2]).group())
                bid_volume = int(re.search(r'\d+', fields[3]).group())
                ask_price = float(re.search(r'\d+', fields[4]).group())
                ask_volume = int(re.search(r'\d+', fields[5]).group())
                records = records + 1
                print("record counter: " + str(records))

                print("LOGGING PRICE: " + timestamp + " " + data)
                
                prices_writer.writerow([timestamp, feedcode, bid_price, bid_volume, ask_price, ask_volume])

            elif data.find("TYPE=TRADE")==0:
                fields = data.split('|')
                feedcode = fields[1][9:]
                side = fields[2][5:]
                traded_price = float(re.search(r'\d+', fields[3]).group())
                traded_volume = int(re.search(r'\d+', fields[4]).group())
                records = records + 1
                print("record counter: " + str(records))

                print("LOGGING TRADE: " + timestamp + " " + data)
                
                trades_writer.writerow([timestamp, feedcode, side, traded_price, traded_volume])

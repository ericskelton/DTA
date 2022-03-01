import socket
from api.utils.log import *
import random

def getQuote(ticker, userid, transactionId):
    #try:
    #    HOST = '192.168.4.2'
    #    PORT = 4444
    #    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #        try:
    #            sock.connect((HOST, PORT))
    #        except socket.error as err:
    #            print('Error connecting to server: {}'.format(err))
#
    #        sock.sendall(ticker.encode()+ b' ' + userid.encode() + b'\n')
    #        data = sock.recv(1024)
    #    decodedData = data.decode().split(',')
#
    #    logJsonObject({
    #        'ticker': ticker,
    #        'price': decodedData[0],
    #        'username': decodedData[1],
    #        'timestamp': decodedData[2],
    #        'cryptographicKey': decodedData[3],
    #        'type': 'quoteServer',
    #        'transactionId': transactionId
    #    })
#
    #    return {
    #        'ticker': ticker,
    #        'price': decodedData[0],
    #        'username': decodedData[1],
    #        'timestamp': decodedData[2],
    #        'cryptographicKey': decodedData[3]
    #    }
    #except Exception as e:
        randomFloat = (random.uniform(0, 1) * 250) + 50
        # generate random key
        from key_generator.key_generator import generate

        key = generate(seed = randomFloat//1)
        return {
            'ticker': ticker,
            # random value from 50 to 300, rounded to 2 decimal places its real ugly i know
            'price': float(str(randomFloat).split('.')[0] +'.' + str(randomFloat).split('.')[1][:2]),
            'username': userid,
            'timestamp': str(int(time.time())),
            'cryptographicKey': key.get_key(),
        }






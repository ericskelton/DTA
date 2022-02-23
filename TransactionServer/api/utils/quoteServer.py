import socket
from api.utils.log import logJson

def getQuote(ticker, userid, transactionId):
    HOST = '192.168.4.2'
    PORT = 4444
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((HOST, PORT))
        except socket.error as err:
            print('Error connecting to server: {}'.format(err))
        
        sock.sendall(ticker.encode()+ b' ' + userid.encode() + b'\n')
        data = sock.recv(1024)
    decodedData = data.decode().split(',')

    logJson({
        'ticker': ticker,
        'price': decodedData[0],
        'username': decodedData[1],
        'timestamp': decodedData[2],
        'cryptographicKey': decodedData[3],
        'type': 'quoteServer',
        'transactionId': transactionId
    })

    return {
        'ticker': ticker,
        'price': decodedData[0],
        'username': decodedData[1],
        'timestamp': decodedData[2],
        'cryptographicKey': decodedData[3]
    }







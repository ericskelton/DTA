import socket

class quoteServer():
    def __init__(self):
        pass

    @staticmethod
    def getQuote(ticker):
        HOST = '192.168.4.2'
        PORT = 4444
        print('Connecting to server at {}:{}'.format(HOST, PORT))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((HOST, PORT))
            except socket.error as err:
                print('Error connecting to server: {}'.format(err))
            print(sock)
            sock.sendall(ticker.encode() + b'\n')
            data = sock.recv(1024)
        decodedData = data.decode().split(',')

        return {
            'ticker': ticker,
            'price': decodedData[0],
            'username': decodedData[1],
            'timestamp': decodedData[2],
            'cryptographicKey': decodedData[3]
        }


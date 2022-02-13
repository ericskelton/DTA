import socket

def getQuote(ticker):
    HOST = '192.168.4.2'
    PORT = 4444
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(ticker.encode())
        data = sock.recv(1024)
    print('Received', repr(data))

def main():
    getQuote('AAPL')
    getQuote('GOOG')
    getQuote('MSFT')

if __name__ == '__main__':
    main()

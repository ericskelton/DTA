import socket

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
        sock.sendall(ticker.encode())
        data = sock.recv(1024)
    print('Received', repr(data))

def main():
    getQuote('AAPL')
    getQuote('GOOG')
    getQuote('MSFT')

if __name__ == '__main__':
    main()

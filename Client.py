import socket, threading, time

def handle_messages(connection: socket.socket):
    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 2009

    while True:
        try:
            msg = connection.recv(1024)

            # If there is no message, there is a chance that connection has closed
            # so the connection will be closed and an error will be displayed.
            # If not, it will try to decode message in order to show to user.
            if msg:
                print(msg.decode())
            else:
                connection.close()
                break

        except Exception as e:
            print(f'Error handling message from server: {e}')
            #try again after 10 seconds, up to 5 times
            for i in range(5):
                try:
                    connection.connect((SERVER_ADDRESS, SERVER_PORT))
                    break
                except Exception as e:
                    print(f'Error connecting to server socket {e}')
                    print('Trying to reconnect in 5 seconds...')
                    time.sleep(5)
                    #try reconnecting
                    client()
            connection.close()
            break

def client() -> None:
    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 2009

    try:
        #Create the socket and start connection with the server
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        #Create a thread in order to handle messages
        threading.Thread(target=handle_messages, args=[socket_instance]).start()

        print('Connected to Event Scheduler Server!')

        # Read user's input until it quit from chat and close connection
        while True:
            msg = input()

            if msg == 'quit':
                break

            # Parse message to utf-8
            socket_instance.send(msg.encode())

        # Close connection with the server
        socket_instance.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        print('Trying to reconnect in 5 seconds...')
        time.sleep(5)
        #try reconnecting
        client()
        #socket_instance.close()


if __name__ == "__main__":
    client()
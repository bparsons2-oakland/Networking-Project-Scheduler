import socket, threading, schedule, time, random

connections = []
event_list = []

def handle_user_connection(connection: socket.socket, address: str) -> None:
    connection.send('Enter password: '.encode())
    password = connection.recv(1024).decode()

    if password != '123':
        connection.send('Wrong password!'.encode())
        connection.close()
        return
    
    while True:
        try:
            connection.send('Welcome to the event scheduler!'.encode())
            connection.send('1 - Make new event'.encode() + '\n'.encode())
            connection.send('2 - See all events'.encode() + '\n'.encode())
            connection.send('3 - Delete an event'.encode() + '\n'.encode())
            connection.send('4 - Edit an event.'.encode() + '\n'.encode())
            connection.send('5 - Exit.'.encode() + '\n'.encode())

            msg = connection.recv(1024)

            if msg:
                msg = msg.decode()

                if msg == '1':
                    connection.send('Enter event name: '.encode())

                    event_name = connection.recv(1024).decode()

                    connection.send('Enter event date (dd/mm/yyyy): '.encode())
                    event_date = connection.recv(1024).decode()

                    while len(event_date) != 10 or event_date[2] != '/' or event_date[5] != '/':
                        connection.send('Invalid date format! Enter event date (dd/mm/yyyy): '.encode())
                        event_date = connection.recv(1024).decode()
                    

                    connection.send('Enter event time (hh:mm, in military time): '.encode())
                    event_time = connection.recv(1024).decode()

                    while len(event_time) != 5 or event_time[2] != ':':
                        connection.send('Invalid time format! Enter event time (hh:mm): '.encode())
                        event_time = connection.recv(1024).decode()

                    #make a random letters id for the event
                    event_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
                    event_list.append((event_name, event_date, event_time, event_id))

                    #make the event run the alert_event function when the time comes
                    schedule.every().day.at(event_time).do(alert_event , event_id)
                elif msg == '2':
                    all_jobs = event_list
                    event_num = 1

                    for job in all_jobs:
                        connection.send(f'{event_num}. Event: {job[0]} | Date: {job[1]} | Time: {job[2]}'.encode())
                        event_num += 1

                    if len(event_list) == 0:
                        connection.send('No events scheduled!'.encode())

                    #take me back to the main menu
                    connection.send('Press any key to go back to the main menu'.encode())
                    connection.recv(1024)

                elif msg == '3':
                    all_jobs = event_list
                    event_num = 1

                    for job in all_jobs:
                        connection.send(f'{event_num}. Event: {job[0]} | Date: {job[1]} | Time: {job[2]}'.encode())
                        event_num += 1

                    if len(event_list) == 0:
                        connection.send('No events scheduled!'.encode())
                        
                    elif len(event_list) != 0:
                        connection.send('Select which event to delete.'.encode())

                        deleteVal = connection.recv(1024).decode()
                        deleteValInt = int(deleteVal) - 1
                        schedule.cancel_job(event_list[deleteValInt][3])
                        event_list.pop(deleteValInt)
                        connection.send('Event deleted.'.encode())


                    connection.send('Press any key to go back to the main menu'.encode())
                    connection.recv(1024)

                elif msg == '4':
                    all_jobs = event_list
                    event_num = 1

                    for job in all_jobs:
                        connection.send(f'{event_num}. Event: {job[0]} | Date: {job[1]} | Time: {job[2]}'.encode())
                        event_num += 1

                    if len(event_list) == 0:
                        connection.send('No events scheduled!'.encode())
                    
                    elif len(event_list) != 0:
                        connection.send('Select which event to edit.'.encode())
                    
                        editVal = connection.recv(1024).decode()
                        editValInt = int(editVal) - 1
                        
                        event_id = event_list[editValInt][3]

                        connection.send('Enter event name: '.encode())

                        event_name = connection.recv(1024).decode()

                        connection.send('Enter event date (dd/mm/yyyy): '.encode())
                        event_date = connection.recv(1024).decode()

                        while len(event_date) != 10 or event_date[2] != '/' or event_date[5] != '/':
                            connection.send('Invalid date format! Enter event date (dd/mm/yyyy): '.encode())
                            event_date = connection.recv(1024).decode()
                        

                        connection.send('Enter event time (hh:mm, in military time): '.encode())
                        event_time = connection.recv(1024).decode()

                        while len(event_time) != 5 or event_time[2] != ':':
                            connection.send('Invalid time format! Enter event time (hh:mm): '.encode())
                            event_time = connection.recv(1024).decode()
                        
                        event_list[editValInt] = (event_name, event_date, event_time, event_id)
                        #make the event run the alert_event function when the time comes
                        schedule.every().day.at(event_time).do(alert_event , event_id)

                elif msg == '5':
                    connection.send('Bye!'.encode())
                    time.sleep(1)
                    connection.close()
                    break

                else:
                    connection.send('Invalid option!'.encode())
                

        except Exception as e:
            print(f'Error: {e}')
            break

def server() -> None:
    threading.Thread(target=run_scheduler).start()

    #Port will be 2009, the year minecraft was released
    Port = 2009
    
    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Allow for multiple connections on the one socket
        socket_instance.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        socket_instance.bind(('', Port))
        socket_instance.listen(4)

        print('Server running!')
        
        while True:

            socket_connection, address = socket_instance.accept()
            connections.append(socket_connection)
            threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()


    except Exception as e:
        print(f'An error has occurred when instancing socket: {e}')

        socket_instance.close()

def run_scheduler() -> None:
    while True:
        schedule.run_pending()
        time.sleep(1)

def alert_event(event_id: str):
    event = [event for event in event_list if event[3] == event_id][0]
    print(f'Event {event[0]} is happening now!')

    #send the message to all connected clients
    for connection in connections:
        connection.send(f'Event {event[0]} is happening now!'.encode())


server()

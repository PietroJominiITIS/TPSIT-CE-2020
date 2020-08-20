from threading import Thread
import socket
import click

def LOG(msg, v=True):
    if v:
        print(msg)

def connection_handler(connection, address, recv_size, log):
    ip, port = address
    identifier = f'[{ip}:{port}]'
    LOG(f'{identifier} % CONNECTED', log)
    with connection:
        receiving = True
        while receiving:
            data = connection.recv(recv_size)
            receiving = bool(data)
            if receiving:
                LOG(f'{identifier} - {data.decode().strip()}', log)
                connection.send(data)
    LOG(f'{identifier} % DISCONNECTED', log)

def mainloop(host, port, recv_size, log):
    THREADED_CONNECTIONS = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen()
        try:
            while True:
                connection, address = sock.accept()
                connection_thread = Thread(target=connection_handler, args=(connection, address, recv_size, log))
                connection_thread.start()
                THREADED_CONNECTIONS.append(connection_thread)
        except KeyboardInterrupt:
            pass
    for threaded_connection in THREADED_CONNECTIONS:
        threaded_connection.join()

@click.command()
@click.option('-h', '--host',           default='127.0.0.1',    help='Host server address',             show_default=True,  type=str)
@click.option('-p', '--port',           default=8888,           help='Host server PORT',                show_default=True,  type=int)
@click.option('-s', '--recv-size',      default=1024,           help='Maximum packet size allowed',     show_default=True,  type=int)
@click.option('-v', '--log-verboose',   is_flag=True,           help='If SET, log connections and data streams to STDOUT')
def cli_passthrough(host, port, recv_size, log_verboose):
    mainloop(host, port, recv_size, log_verboose)

if __name__ == '__main__':
    cli_passthrough()
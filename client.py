import socket
import click
import protocol

def TCP_send(host, port, data, wait_response, response_size):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as link:
        link.connect((host, port))
        link.send(data.encode())
        if wait_response:
            response = link.recv(response_size)
            payload = response.decode()
            data = protocol.decode(payload)
            print(data)

@click.command()
@click.argument('data')
@click.option('-h', '--host',           default='127.0.0.1',    help='Host server address',             show_default=True,  type=str)
@click.option('-p', '--port',           default=8888,           help='Host server PORT',                show_default=True,  type=int)
@click.option('-t', '--dtype',          default='str',          help='Data type',                       show_default=True,  type=click.Choice(['str', 'int']))
@click.option('-s', '--response-size',  default=1024,           help='Maximum response size allowed',   show_default=True,  type=int)
@click.option('-w', '--wait-response',  is_flag=True,           help='If SET, wait for the server response and print it to STDOUT')
def cli_passthrough(data, host, port, dtype, wait_response, response_size):
    if dtype == 'int':
        try:
            data = int(data)
        except ValueError:
            print("WARNING: DATA Can't be converted to integer. It will be used as string")
    payload = protocol.encode(data)
    TCP_send(host, port, payload, wait_response, response_size)

if __name__ == '__main__':
    cli_passthrough()
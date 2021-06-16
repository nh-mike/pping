import argparse
import os
import socket
import sys
import time

protocols = {
    "ftp": 21,
    "ssh": 22,
    "telnet": 23,
    "smtp": 25,
    "dns": 53,
    "dhcp": 67,
    "tftp": 69,
    "http": 80,
    "pop3": 110,
    "imap": 143,
    "ldap": 389,
    "https": 443,
    "ftps": 990,
    "rdp": 3389
}


def main():
    # Method name is too long, trying to keep my code tidy within 79 characters
    ap = argparse.ArgumentParser
    examples = helpExamples()

    psr = ap(formatter_class=argparse.RawTextHelpFormatter,
             description='Connect to a network port to determine if a server' +
                         ' / service is accessible',
             epilog=examples,
             prefix_chars='-')

    psr.add_argument('-t',
                     action='store_true',
                     help='Continuously attempt to connect to the port until' +
                     ' stopped This option is incompatible with -n' + "\r\n" +
                     'To stop, use Control + C',
                     dest="forever")

    psr.add_argument('-n',
                     nargs=1,
                     type=int,
                     help='The number of times to attempt to connect to the ' +
                     'port. This option is incompatible with -t',
                     dest="count")

    psr.add_argument('-w',
                     nargs=1,
                     type=int,
                     default=1000,
                     help='Time to wait in milliseconds to wait before ' +
                     'trying again',
                     dest="timeout")

    psr.add_argument('address',
                     metavar='ADDRESS',
                     type=str,
                     help='An IP Address or a Domain Name to target')

    psr.add_argument('port',
                     metavar='PORT',
                     type=str,
                     help='Port Number or a Protocol Name. See list of ' +
                     'Supported Protocol Names below')

    args = psr.parse_args()

    address = validate_address(args.address)
    port = validate_port(args.port)
    count = validate_count(args.forever, args.count)
    timeout = validate_timeout(args.timeout)

    while count != 0:
        try:
            result = doPPing(address, port)
            count -= 1
            if count != 0:
                time.sleep(timeout)
        except KeyboardInterrupt:
            break

    sys.exit(result)


def doPPing(address, port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (address, int(port))
    result_of_check = a_socket.connect_ex(location)
    a_socket.close()

    if result_of_check == 0:
        print("Port " + str(address) + ':' + str(port) + " is open")
        return 0
    else:
        print("Port " + str(address) + ':' + str(port) + " is not open")
        return 1


def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # inet_pton doesn't exist
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True


def validate_address(address):
    if (
        is_valid_ipv4_address(address) is not True and
        is_valid_ipv6_address(address) is not True
    ):
        try:
            (_, _, a) = socket.gethostbyname_ex(address)
            address = a[0]
        except:
            raise FatalException(
                '% is not a valid IP address or DNS records do not exist'
                % address)

    return address


def is_valid_port_number(port):
    if 1 <= port <= 65535:
        return True
    else:
        return False


def validate_port(port):
    try:
        port = int(port)
    except:
        port = protocols[port.lower()]

    if is_valid_port_number(port) is not True:
        raise FatalException(port + ' is not a valid port number (1-65535)')

    return port


def validate_count(forever, count):
    if forever is True and count is not None:
        raise FatalException('Cannot use -n and -t together')
    if forever is True:
        return -1
    elif count is None:
        return 1
    elif count[0] > 0:
        return count[0]
    else:
        raise FatalException('Cannot set count to zero')


def validate_timeout(timeout):
    if timeout is None:
        return 1
    else:
        return timeout/1000


def helpExamples():
    op = ''
    selfname = '  ' + os.path.basename(sys.argv[0])
    minpad = 1
    ps = {
        'PROTOCOL': 'PORT'
    }

    for key in protocols:
        ps[key] = protocols[key]

    for key in ps:
        if len(key) > minpad:
            minpad = len(key)

    minpad = minpad + 2

    op = op + 'examples:' + "\r\n"
    op = op + selfname + ' 8.8.8.8 53' + "\r\n"
    op = op + selfname + ' dns.google.com dns' + "\r\n"
    op = op + selfname + ' 142.250.66.238 80' + "\r\n"
    op = op + selfname + ' google.com http' + "\r\n"
    op = op + selfname + ' 142.250.66.238 443' + "\r\n"
    op = op + selfname + ' google.com https' + "\r\n"
    op = op + "\r\n"
    op = op + 'supported protocol names:' + "\r\n"

    for key in ps:
        op = op + '  ' + str(key.ljust(minpad) + str(ps[key]) + "\r\n")

    op = op + "\r\n"
    op = op + 'This software is licensed under the LGPL-3.0 license.' + "\r\n"
    op = op + 'https://github.com/nh-mike/pping/blob/main/LICENSE'
    return op


class FatalException(Exception):
    pass


if __name__ == "__main__":
    try:
        main()
    except FatalException as error:
        print(repr(error))

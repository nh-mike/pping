import os
import socket
import sys

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


def main(address, port):
    address = validate_address(address)
    port = validate_port(port)

    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    location = (address, int(port))
    result_of_check = a_socket.connect_ex(location)
    a_socket.close()

    if result_of_check == 0:
        print("Port " + str(address) + ':' + str(port) + " is open")
    else:
        print("Port " + str(address) + ':' + str(port) + " is not open")


def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
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


def help():
    selfname = os.path.basename(sys.argv[0])
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

    print('"Port Ping"')
    print('Connect to a network port to determine if a server / ' +
          'service is accessible')
    print('')
    print('Usage')
    print(selfname + ' ADDRESS PORT')
    print('')
    print('ADDRESS:')
    print('For the ADDRESS option, you can supply an IP address or ' +
          'a Domain Name')
    print('')
    print('PORT:')
    print('For the PORT option, you can supply a Port Number or a ' +
          'Protocol Name')
    print('See list of Supported Protocol Names below')
    print('')
    print('EXAMPLES:')
    print(selfname + ' 8.8.8.8 53')
    print(selfname + ' dns.google.com dns')
    print(selfname + ' 142.250.66.238 80')
    print(selfname + ' google.com http')
    print(selfname + ' 142.250.66.238 443')
    print(selfname + ' google.com https')
    print('')
    print('Supported Protocol Names:')

    for key in ps:
        print(key.ljust(minpad) + str(ps[key]))


class FatalException(Exception):
    pass


if __name__ == "__main__":
    if len(sys.argv) == 3:
        try:
            main(sys.argv[1], sys.argv[2])
        except FatalException as error:
            print(repr(error))
    else:
        help()

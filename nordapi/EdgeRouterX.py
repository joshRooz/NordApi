import OpenVpnUdp
import sys
import getopt
import fileinput


def main(argv):
    country = None
    try:
        opts, args = getopt.getopt(argv, "hc", ["country="])
    except getopt.GetoptError:
        print('EdgeRouterX.py -c <country>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('EdgeRouterX.py -c <country>')
            sys.exit()
        elif opt in ("-c", "--country"):
            country = arg

    assert type(country) == str, 'Invalid Country: EdgeRouterX.py -h'

    # 1. Download the recommended config file from NordVPN
    uk = OpenVpnUdp.OpenVpnUdp()
    ovpn = uk.get_file(country)

    # 2. Replace the inline username and password fields with a file path
    #    Disable ability for OpenVPN provider to change routes in the firewall
    with fileinput.FileInput(ovpn, inplace=True) as file:
        for line in file:
            line = line.replace(
                'auth-user-pass',
                'auth-user-pass /config/user-data/openvpn/nordvpnauth.txt'
            )
            line = line.replace(
                'pull',
                'pull\nroute-nopull'
            )
            print(line, end='')


if __name__ == "__main__":
    main(sys.argv[1:])

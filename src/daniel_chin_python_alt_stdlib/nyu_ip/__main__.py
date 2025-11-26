from .entries import entries
from local_ip import getLocalIP

def main():
    ips = getLocalIP()
    ips = [x for x in ips if not x.startswith('192.')]
    for ip in ips:
        try:
            print('You are at:', ip, entries[ip])
        except KeyError:
            print('unknown IP:', ip)
            print()
            print('explorer', '\\'.join(__file__.split('\\')[:-1]))
    input('Enter...')

main()

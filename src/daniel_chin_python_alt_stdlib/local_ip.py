'''
Find out local IP addr on Windows
'''
import platform
if platform.system() != 'Windows':
    print('Warning: getLocalIP only works on Windows. ')
    def getLocalIP():
        return []
else:
    import subprocess

    def getLocalIP():
        ip_config = subprocess.check_output('ipconfig').decode('gbk')
        potential_ip = []
        for line in ip_config.split('\r\n'):
            if 'IPv4' in line:
                potential_ip.append(line.split(': ')[1])
        return potential_ip

if __name__ == '__main__':
    print(getLocalIP())
    input('enter...')

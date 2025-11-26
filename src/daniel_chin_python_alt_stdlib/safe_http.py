'''
An HTTP backend server.  
Really tries to be safe against injection attacks.  
Intentionally uses single thread only.  
Only answers GET. Does not abide by request http header fields.  
Does not defend against DoS.  
Problems:  
* socket.send without timeout. Could block the entire scheduling.  
'''
from socket import socket, timeout, gethostname, gethostbyname
from local_ip import getLocalIP
import os
from interactive import inputUntilValid
from time import asctime
from multi_term import TerminalThreePack
from io import BytesIO
from time import time

ACCEPT_TIMEOUT = .005
HANDLE_TIMEOUT = .1
LISTEN = 1
TOP_SPEED = [2 * 1024 * 1024, '2 MB']
PAGE = int(ACCEPT_TIMEOUT * TOP_SPEED[0])

options = {
    'max_connections': (32, '"" if not x else int(x)', 'x == "" or x > 0'), 
    'port': (80, '"" if not x else int(x)', 'x == "" or x > 0'), 
}

def main(Handler, app_name = 'Safe HTTP', log_dir = None, **kw):
    '''
    `Handler` is a class whose following methods you can override:  
        __init__(self, request, sock, addr, time_out, debug, info, warning):  
            Should be non-blocking.  
        prepareResponse(self, debug, info, warning):  
            Prepare the `self.response_content`.  
            Set `self.content_length`.  
            Should return sooner than `self.time_out`.  
            Return 'wait' to indicate job not done yet. You will be re-elected to execute `prepareResponse()`.  
            Return 'done' to indicate job complete. Call unlink yourself.  
            Return 'close' to demand the socket to be closed and removed.  
            Risk of spinlock: The main loop try-waits. Do not do nothing and return 'wait'.  
        unlink(self):  
            called to release files.  
    '''
    terminals, debug, info, warning = initTerminals(app_name, log_dir)
    try:
        info.print('socket read is maxed at', PAGE // 1024, 'KB, allowing', TOP_SPEED[1], '/ s under ACCEPT_TIMEOUT =', ACCEPT_TIMEOUT, 's.')
        loadOptions(kw, info)
        serverSock = socket()
        serverSock.bind(('', options['port']))
        serverSock.listen(LISTEN)
        local_ip = getLocalIP()
        if not local_ip:
            local_ip = [gethostname()]
            local_ip.append(gethostbyname(local_ip[0]))
        info.print('listening at', local_ip, '...')
        try:
            loop(serverSock, Handler, debug, info, warning)
        except KeyboardInterrupt:
            RECEIVED_CTRL_C = 'Received ^C. '
            info.print(RECEIVED_CTRL_C)
            print(RECEIVED_CTRL_C)
        finally:
            force(serverSock.close, debug, info, warning)
        info.print('Exiting main(). ')
    except Exception as e:
        warning.exception()
        raise e

def initTerminals(app_name, log_dir):
    log_dir = log_dir or os.getcwd()
    log_time_dir = os.path.join(log_dir, asctime().replace(':', '-').replace(' ', '_'))
    print('Log file will be at', log_time_dir)
    if inputUntilValid('Is that OK?', 'yn') != 'y':
        raise Exception('User chose to abort.')
    os.mkdir(log_time_dir)
    terminals = TerminalThreePack(app_name, log_time_dir)
    return terminals, terminals['debug'], terminals['info'], terminals['warning']

def loadOptions(kw, info):
    print('Loading options...')
    for key, (default, legalize, validator) in [*options.items()]:
        try:
            options[key] = kw[key]
        except KeyError:
            print(f'`{key}` not provided. ENTER to default `{key} = {default}`.')
            options[key] = inputUntilValid('Otherwise, input value: ', lambda x: eval(validator), legalize = lambda x: eval(legalize))
            if options[key] == '':
                options[key] = default
    info.print('Launching with options: {', *[f'\n\t{k}\t: {v}' for k, v in options.items()], '\n}')
    print('OK. ')

class Client:
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        self.buffer = b''
        self.handler = None

def loop(serverSock, Handler, debug, info, warning):
    info.print('Starting main loop.')
    clients = []
    try:
        sleep = False
        while True:
            # Single thread, try_wait logic
            if len(clients) < options['max_connections']:
                if sleep != all([x.handler is None for x in clients]):
                    sleep = not sleep
                    if sleep:
                        info.print('Switching to sleep mode. ')
                        serverSock.settimeout(1)
                    else:
                        info.print('Switching to awake mode. ')
                        serverSock.settimeout(ACCEPT_TIMEOUT)
                try:
                    sock, addr = serverSock.accept()
                    info.print(addr, 'Accepted. ')
                    clients.append(Client(sock, addr))
                    debug.print('Now we have', len(clients), 'clients. ')
                    sock.settimeout(HANDLE_TIMEOUT)
                except timeout:
                    pass
            for i, client in reversed([*enumerate(clients)]):
                if client.handler is None:
                    try:
                        debug.print(client.addr, 'Receiving request...')
                        recved = client.sock.recv(PAGE)
                        assert recved != b''
                    except timeout:
                        continue
                    except AssertionError:
                        unlink(clients, i, debug, info, warning)
                        continue
                    except Exception as e:
                        info.print(client.addr, 'Shutdown with unknown exception', e)
                        warning.exception()
                        unlink(clients, i, debug, info, warning)
                        continue
                    client.buffer += recved
                    splited = client.buffer.split(b'\r\n\r\n', 1)
                    if len(splited) > 1:
                        byte_request, client.buffer = splited
                        request = Request(byte_request, debug, info, warning)
                        if request.valid:
                            info.print(client.addr, 'request parsed. ')
                            debug.print(client.addr, request)
                            client.handler = Handler(request, client.sock, client.addr, HANDLE_TIMEOUT, debug, info, warning)
                            client.sock.settimeout(None)
                        else:
                            warning.print(client.addr, 'invalide request. ')
                            unlink(clients, i, debug, info, warning)
                            continue
                    else:
                        warning.print(client.addr, 'sent partial request. Waiting for more... ')
                if client.handler is not None:
                    debug.print('do begin')
                    result = client.handler.do(debug, info, warning)
                    debug.print('do end')
                    if result == 'done':
                        client.handler = None
                    elif result == 'close':
                        info.print('Handler of', addr, 'demanded shutdown.')
                        unlink(clients, i, debug, info, warning)
                        continue
                    elif result == 'wait':
                        pass
                    else:
                        raise ValueError(f'Handler of {addr} returned invalid value: {result}')
    finally:
        while clients:
            unlink(clients, 0, debug, info, warning)

def force(function, debug, info, warning):
    try:
        function()
    except Exception as e:
        warning.print('`force` ignoring', e)

class Request:
    def __init__(self, segment, debug, info, warning):
        self.valid = False
        try:
            lines = segment.decode().split('\r\n')
        except UnicodeDecodeError:
            warning.print('Request does not decode into str.')
            return
        try:
            parsing = lines.pop(0)
            (
                self.command, 
                self.target, 
                self.http_version, 
            ) = parsing.split(' ')
            if self.command != 'GET':
                parsing = sanitize(parsing, 'Escaped sequence found in request! ')
                warning.print('Ignoring non-GET request:', parsing)
                return
            self.header_fields = {}
            for parsing in lines:
                kw, value = parsing.split(':', 1)
                self.header_fields[kw.strip(' ')] = value.strip(' ')
        except Exception as e:
            warning.print('Request has bad line:', parsing)
            return
        self.valid = True
    
    def __str__(self):
        return self.command + ' ' + self.target

def unlink(clients, i, debug, info, warning):
    addr = clients[i].addr
    debug.print('Closing', addr)
    force(clients[i].sock.close, debug, info, warning)
    clients[i].handler and clients[i].handler.unlink()
    clients.pop(i)
    info.print(addr, 'Closed. ')
    debug.print('Remaining:', len(clients), 'clients. ')

class BaseHandler:
    def __init__(self, request, sock, addr, time_out, debug, info, warning):
        self.request = request
        self.sock = sock
        self.addr = addr
        self.time_out = time_out
        self.response_content = BytesIO()
        self.response_ready = False
        self.content_length = None
        self.content_type = 'text/html'
    
    def do(self, debug, info, warning):
        if self.response_ready:
            debug.print(self.addr, 'serving response...')
            return self.serveResponse(debug, info, warning)
        debug.print(self.addr, 'preparing response...')
        result = self.prepareResponse(debug, info, warning)
        if result == 'done':
            self.respondHead(self.content_length)
            self.response_ready = True
            return self.do(debug, info, warning)
        else:
            return result
    
    def prepareResponse(self, debug, info, warning):  
        '''
        Override this method
        '''
        self.response_content.write(b"What a shame! The programmer didn't override `prepareResponse()`.")
        self.content_length = self.response_content.tell()
        self.response_content.seek(0)
        return 'done'
    
    def serveResponse(self, debug, info, warning):
        when_stop = time() + self.time_out
        n_cycles = 0
        while time() < when_stop:
            n_cycles += 1
            data = self.response_content.read(PAGE)
            if not data:
                info.print(self.addr, 'is responded.')
                return 'close'
            try:
                n_bytes_sent = self.sock.send(data)
            except (ConnectionAbortedError, ConnectionResetError):
                info.print(self.addr, 'remote shutdown. ')
                return 'close'
            self.response_content.seek(
                self.response_content.tell() \
                - len(data) + n_bytes_sent, 
            )
        debug.print(f'1 timeout + {format(time() - when_stop, ".1f")} s = {n_cycles} cycles. ')
        debug.print(self.addr, 'progress', format(self.response_content.tell() / self.content_length * 100, '.1f') + '%')
        return 'wait'
    
    def unlink(self):
        '''
        Override this method
        '''
        ...

    def respondHead(self, content_length):
        response = f'''HTTP/1.1 200 OK\r
Content-Length: {content_length}\r
Content-Type: {self.content_type}\r\n\r\n'''
        self.sock.send(response.encode())

if __name__ == '__main__':
    main(BaseHandler)

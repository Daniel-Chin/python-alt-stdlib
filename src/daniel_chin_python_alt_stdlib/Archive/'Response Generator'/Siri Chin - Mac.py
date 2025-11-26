import socket
class con:
    display=5
    window_height=18
    msg_len=1000
def cls():
    print(chr(10)*20)
def refresh(history,state):
    cls()
    if state=="idle":
        print("="*6,"   Siri Chin   ","="*6)
    elif state=="listening":
        print("="*6," Calculating... ","="*6)
    else:
        print("Error: Invalid state. Press Enter to exit app. ")
        print(input())
        safe_exit()
    print("Siri Chin:  Ask me anything. ")
    for dialog in history[max(len(history)-con.display,0):len(history)]:
        print("Zane Fadul: ",dialog[0])
        print("Siri Chin:  ",dialog[1])
        print("")
    blank=con.window_height-3*len(history)-2
    if blank>=0:
        for i in range(blank):
            print("")
def Zane_speak():
    print("/^^^^^^^^^^^")    
    return input("| ")
def get_answer(question,socket):
    blank=con.msg_len-len(question)
    if blank<0:
        print("Error: Your question is too long, Siri Chin crashed. ")
        print(input())
        safe_exit()
    question+=" "*blank
    totalsent = 0
    while totalsent < con.msg_len:
        sent = socket.send(question[totalsent:].encode("utf-8"))
        if sent == 0:
            print("Fatal Error 1. ")
            print(input())
            safe_exit()
        totalsent += sent
    # Asked.  
    chunks = []
    bytes_recd = 0
    while bytes_recd < con.msg_len:
        chunk = socket.recv(min(con.msg_len - bytes_recd, 2048)).decode("utf-8")
        if chunk == '':
            print("Fatal Error 2. ")
            print(input())
            safe_exit()
        chunks.append(chunk)
        bytes_recd += len(chunk)
    return ''.join(chunks)
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("LAPTOP-U0NOJH1G", 2333))
    return s
def safe_exit():
    socket.close
    exit()
#
# Main
socket=connect()
history=[]
wanna_exit=False
while not wanna_exit:
    refresh(history,"idle")
    question=Zane_speak()
    if "vocado" in question:
        wanna_exit=True
    else:
        history.append((question,"Generating response... "))
        refresh(history,"listening")
        history[len(history)-1]=(question,get_answer(question,socket))
socket.close()

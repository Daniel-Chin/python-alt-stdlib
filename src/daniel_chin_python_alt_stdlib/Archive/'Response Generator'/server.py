import os
import socket
import winsound
class con:
    display=5
    window_height=18
    msg_len=1000
def cls():
    os.system("cls")
def refresh(history,state):
    cls()
    if state=="idle":
        print("="*6,"   server   ","="*6)
        os.system("title server")
    elif state=="listening":
        print("="*6," Waiting for Zane ","="*6)
        os.system("title Waiting for Zane...")
    else:
        print("Error: Invalid state. Press Enter to exit app. ")
        os.system("pause")
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
def Zane_speak(do_send,answer,socket):
    if do_send:
        blank=con.msg_len-len(answer)
        if blank<0:
            print("Error: Your answer is too long, Siri Chin crashed. ")
            os.system("pause")
            safe_exit()
        answer+=" "*blank
        totalsent = 0
        while totalsent < con.msg_len:
            sent = socket.send(answer[totalsent:].encode("utf-8"))
            if sent == 0:
                print("Fatal Error. ")
                os.system("pause")
                safe_exit()
            totalsent += sent
    # Answered. 
    chunks = []
    bytes_recd = 0
    while bytes_recd < con.msg_len:
        chunk = socket.recv(min(con.msg_len - bytes_recd, 2048)).decode("utf-8")
        if chunk == '':
            print("Fatal Error. ")
            os.system("pause")
            safe_exit()
        chunks.append(chunk)
        bytes_recd += len(chunk)
    return ''.join(chunks)
def get_answer():
    print("/^^^^^^^^^^^")    
    return input("| ")
#    return "Oops! An error occurred. Please contact Daniel for help. "
def serve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("LAPTOP-U0NOJH1G", 2333))
    s.listen(1)
    (clientsocket, address) = s.accept()
    #os.system("explorer D:\Res\Alarm.mp3")
    '''
    winsound.Beep(880, 1000)
    winsound.Beep(1760, 1000)
    winsound.Beep(1760, 1000)
    winsound.Beep(880, 1000)
    '''
    return clientsocket
def safe_exit():
    socket.close
    exit()
#
# Main
socket=serve()
history=[]
answer=""
#########
refresh(history,"listening")
question=Zane_speak(False,answer,socket)
history.append((question,"Generating response... "))
refresh(history,"idle")
answer=get_answer()
history[len(history)-1]=(question,answer)
#########
while 1:
    refresh(history,"listening")
    question=Zane_speak(True,answer,socket)
    history.append((question,"Generating response... "))
    refresh(history,"idle")
    answer=get_answer()
    history[len(history)-1]=(question,answer)
socket.close()

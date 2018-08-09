from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread 
import tkinter

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            main.msg_list.insert(tkinter.END, msg)
        except OSError: 
            break

def send(event=None):
    msg = main.my_msg.get()
    main.my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    """To be called to close window"""
    main.my_msg.set("{quit}")
    send()

def new_winF(): # new window definition
    
    name = main.my_msg.get()
    newwin = tkinter.Toplevel(top)
    jotter = Window(newwin, name)

    def jot(event=None):
        note = jotter.my_msg.get()
        jotter.my_msg.set("")
        jotter.msg_list.insert(tkinter.END, note)

    jotter.send_button = tkinter.Button(newwin, text="Note", command = jot)
    jotter.entry_field.bind("<Return>", jot)
    jotter.send_button.pack()


    

    
class Window:

    def __init__(self, root, title):
        root.title(title)
        self.messages_frame = tkinter.Frame(root)
        self.my_msg = tkinter.StringVar()
        self.my_msg.set("Type your messages here.")
        self.scrollbar = tkinter.Scrollbar(self.messages_frame)
        
        self.msg_list = tkinter.Listbox(self.messages_frame, height = 15, width = 50, yscrollcommand = self.scrollbar.set)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.msg_list.pack(side=tkinter.LEFT, fill = tkinter.BOTH)
        self.msg_list.pack()
        self.messages_frame.pack()

        self.entry_field = tkinter.Entry(root, textvariable=self.my_msg)
        self.entry_field.pack()
 

# --------Main window -------------


top = tkinter.Tk()
main = Window(top, "Chatter")

main.send_button = tkinter.Button(top, text="Send", command = send)
main.send_button.pack()
main.branch_button = tkinter.Button(top, text = "Branch", command = new_winF)
main.branch_button.pack()
main.entry_field.bind("<Return>", send)

top.protocol("WM_DELETE_WINDOW", on_closing)

#-------Sockets------------------

HOST = input("Enter host: ")
PORT = input("Enter port: ")

if not PORT:
    PORT = 33000 #Default
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target = receive)
receive_thread.start()
tkinter.mainloop()

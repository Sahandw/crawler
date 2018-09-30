#Sahand Akbari



from tkinter import *
import socket

#Showing the result returning from the server
def show(parent , result):
    top = Toplevel(parent )
    w = 400
    h = 250

    sw  = top.winfo_screenwidth()
    sh = top.winfo_screenheight()

    x = (int)(sw - w) / 2
    y = (int)(sh - h) / 2

    top.geometry(("%dx%d+%d+%d" % (w,h,x,y)))
    top.resizable(width=False,height=False)

    sb = Scrollbar(top)
    sb.pack(side = RIGHT , fill = Y)

    sb2 = Scrollbar(top , orient = HORIZONTAL)
    sb2.pack(side = BOTTOM , fill = X)



    listbox = Listbox(top)
    listbox.pack()
    listbox.config(width = 400 , height = 200)


    for res in result:
        listbox.insert(END, ">>>" +res)


    listbox.config(yscrollcommand = sb.set)
    listbox.config(xscrollcommand = sb2.set)
    sb.config(command = listbox.yview)
    sb2.config(command = listbox.xview)

    top.mainloop()


# Main class of application
class Application(Frame):
    def __init__(self,parent):
        Frame.__init__(self)

        self.parent = parent

        self.initUI()

    def centerWindow(self):
        w = 450
        h = 250

        sw  = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (int)(sw - w) / 2
        y = (int)(sh - h) / 2

        self.parent.geometry(("%dx%d+%d+%d" % (w,h,x,y)))
        self.parent.resizable(width=False,height=False)

    def initUI(self):
        self.parent.title("Client")
        self.pack(fill = BOTH , expand = 1)

        self.centerWindow()

        lbl = Label(self,text = "URL:")
        lbl.place(x = 20,y=25)
        lbl2 = Label(self,text = "Depth:")
        lbl2.place(x = 20 , y = 97)
        lbl4 = Label(self,text = "Keyword:")
        lbl4.place(x = 20 , y = 170)



        self.url = Entry(self)
        self.url.place(x= 80 ,y =20 ,width = 160 , height = 25)

        self.depth = Entry(self)
        self.depth.place(x = 80, y = 95 , width = 40 , height = 25)


        self.keyword = Entry(self)
        self.keyword.place(x = 80, y = 170 , width = 160 , height = 25)


        self.mailb = Button(self,text="Find the Emails",
                       command = self.mbhandler)
        self.mailb.place(x = 300 , y = 160)

        self.linkb = Button(self,text="Find the Links" ,
                       command = self.lbhandler)
        self.linkb.place(x = 300 , y = 100)

        self.searchb = Button(self,text = "serach for the Keyword" , command = self.sbhandler)
        self.searchb.place(x = 300 , y = 40)
    # handler for clicking on the search button
    def sbhandler(self):
        print("On Search Button Clicked...")
        print("Starting the Search...")

        url = self.url.get()
        depth = self.depth.get()
        keyword = self.keyword.get()


        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = 'localhost'
        port = 8989
        s.connect((host,port))
        msg = 'search' + ',' +  url + ','+ keyword + ',' + depth
        s.send(bytes(msg , 'utf-8'))
        data = s.recv(90000000)
        show(self.parent, [data.decode('utf-8')])
        s.close()



    # handler for clicking on the get the links button
    def lbhandler(self):
        print("On Links Button Clicked...")
        print("finding the Links ... ")

        url = self.url.get()
        depth = self.depth.get()

        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = 'localhost'
        port = 6767
        s.connect((host,port))
        msg = url + ',' + depth
        s.send(bytes(msg , 'utf-8'))
        data = s.recv(90000000)
        s.close()
        answer = data.decode('utf-8').split("* *")
        show(self.parent,answer)
        print("Recieved from Server: " , data)




    # handler for clicking on the get the mail buttons
    def mbhandler(self):
        print("On Mail Button Clicked")
        print("Finding the Mail Adresses")


        depth = self.depth.get()
        url = self.url.get()


        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = 'localhost'
        port = 7878
        s.connect((host,port))
        msg = ('mails', url , depth)
        msg = ','.join(msg)
        s.send(bytes(msg,'utf-8'))
        data = s.recv(90000000)
        s.close()

        answer = data.decode('utf-8').split("* *")
        show(self.parent,answer)
        print("Recieved from Server: " , data)





# creating the gui loop
def main():
    root = Tk()
    app = Application(root)



    root.mainloop()



if __name__ == '__main__':
    main()




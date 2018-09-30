# Sahand Akbari



import socket
import threading
from bs4 import *
from urllib.request import *
import re
from queue import *



# This class handles the requests for Link search

class LinkThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverSocket.bind(('localhost' , 6767))
        serverSocket.listen(5)
        while True:
            conn , addr  = serverSocket.accept()
            print('connected by address : ' , addr)
            data = conn.recv(90000000)
            msg = ""
            str = data.decode('utf-8')
            list = str.split(',')
            url = list[0]
            depth = int(list[1])
            for link in self.findLinks(url,depth):
                msg += "* *" + link
            try:
                print(msg)
            except Exception as e:
                print(e)
            print(str , type(str))
            conn.send(bytes(msg , 'utf-8'))

        serverSocket.close()


    # returns all the links of a url and its children when the depth is given
    def findLinks(self , url, depth ,Q = Queue()):

        s = set() # links in the current depth
        final = set() # final set of links to be returned
        s.add(url)
        final.add(url)



        for i in range(0,depth):
            tempLinks = []
            removeLinks = []
            for l in s:
                removeLinks.append(l)
                if 'http' in l or 'www' in l:
                    newLinks = self.getLinks(url)
                else:
                    newLinks = self.getLinks(url + l)
                for link in newLinks:
                    final.add(link)
                    Q.put(link)
                    tempLinks.append(link)
            for l in tempLinks:
                s.add(l)
            for l in removeLinks:
                s.remove(l)
        return final

    # returns all the links found on a url
    def getLinks(self , url):
        res = []
        try:
            html = urlopen(url)
        except Exception as ex:
            try:
                print("OOoops Something happened ! let's move on >>>>" , url)
            except Exception as e:
                print(e)
            list = []
            return list
        soup = BeautifulSoup(html,'html.parser')
        links = (soup.findAll('a' , {'href' : re.compile("^.*$")}))
        for l in links:
            res.append(l.attrs['href'])

        return res


# this class handles the requests for keyword search
class SearchThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverSocket.bind(('localhost' , 8989))
        serverSocket.listen(5)
        while True:
            conn , addr  = serverSocket.accept()
            print('connected by address : ' , addr)
            data = conn.recv(1024)
            msg = ""
            str = data.decode('utf-8')
            stringList = str.split(',')
            url = stringList[1]
            keyword = stringList[2]
            depth = int(stringList[3])
            Q = Queue()
            Q.put(url)
            answer = self.search(url,depth,keyword,Q)
            #print(str , type(str))
            conn.send(bytes(answer,'utf-8'))

        serverSocket.close()

    # returns true if a keyword is found on a webpage and its children given the depth
    def search (self,url,depth,keyword,Q):
        answer = "Nothing Found!"
        l = LinkThread()
        l.findLinks(url,depth - 1,Q=Q)
        while not Q.empty():
            try:
                link = Q.get()
                if 'http' in link or 'www' in link:
                    if self.getKeyword(urlopen(link) , keyword):
                        answer = link
                        break
                else:
                    if self.getKeyword(urlopen(url + link) , keyword):
                        answer = link
                        break
            except Exception as ex:
                print("Ooops Something happened here. Let's move on !")
        print(answer)
        return answer



    # returns true if the keyword is found on a page

    def getKeyword(self,html , keyword):
        soup = BeautifulSoup(html,'html.parser')
        regex = re.compile(keyword)
        if (re.findall(regex, soup.getText())):
            return True



# this class handles the requests for Mail search
class MailThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serverSocket.bind(('localhost' , 7878))
        serverSocket.listen(5)
        while True:
            conn , addr  = serverSocket.accept()
            print('connected by address : ' , addr)
            data = conn.recv(90000000)
            str = data.decode('utf-8')
            print(str , type(str))
            msg = ""
            stringList = str.split(',')
            url = stringList[1]
            depth = int(stringList[2])
            answerSet = self.getEmails(url,depth)
            if len(answerSet) == 0:
                msg += "                            Nothing Found !"

            for link in answerSet:
                msg += "* *" + link

            conn.send(bytes(msg,'utf-8'))

        serverSocket.close()

    # returns all the emails in a given url and all its children up to a given depth
    def getEmails(self , url , depth):
        mails = set() # no duplicates allowed
        l = LinkThread()
        # grab all the links on the depth - 1
        #and go to those pages to find the needed emails
        links = l.findLinks(url,depth - 1)
        for q in links:
            try:
                if 'http' in q or 'www' in q:
                    # external links
                    for m in self.findEmails(urlopen(q)):
                        mails.add(m)
                else:
                    # internal links
                    for m in self.findEmails(urlopen(url+q)):
                        mails.add(m)

            except Exception as e:
                print("OOoops, Can't open the Page. let's move on ")

        return mails

    # return all the emails in a certain webpage
    def findEmails(self,html):

        soup = BeautifulSoup(html,'html.parser')
        regex = re.compile("[\w.]+@[\w.]+\.[\w.]+", re.IGNORECASE)
        try:
            print(re.findall(regex,soup.getText()))
        except Exception as e:
            print(e)
        return re.findall(regex,soup.getText())


# in function main all the threads start working
# and listening to receive the proper request

def main():
    link = LinkThread()
    link.start()
    search = SearchThread()
    search.start()
    mail = MailThread()
    mail.start()


if __name__ == '__main__':
    main()

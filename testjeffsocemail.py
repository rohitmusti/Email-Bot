# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 13:50:45 2019

@author: Corey
"""

# d8b   db d88888b d888888b db   d8b   db  .d88b.  d8888b. db   dD .d8888.
# 888o  88 88'     `~~88~~' 88   I8I   88 .8P  Y8. 88  `8D 88 ,8P' 88'  YP
# 88V8o 88 88ooooo    88    88   I8I   88 88    88 88oobY' 88,8P   `8bo.
# 88 V8o88 88~~~~~    88    Y8   I8I   88 88    88 88`8b   88`8b     `Y8b.
# 88  V888 88.        88    `8b d8'8b d8' `8b  d8' 88 `88. 88 `88. db   8D
# VP   V8P Y88888P    YP     `8b8' `8d8'   `Y88P'  88   YD YP   YD `8888Y'

# Don't use pythons SMTP library, implement the application level socket
# yourself.


import sys
import socket
import csv

BUFFER_SIZE = 1024


def sendMessage(smtpServer, port, fromAddress, toAddress, message):

        # Open socket on port

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((smtpServer, int(port)))

        # display response
        print(s.recv(1024).decode())

        # Send HELO fake.fr

        # could be any fake address space here (even fake.fr) I chose virginia.edu
        # for consistency with fake email
        heloMessage = 'HELO virginia.edu\r\n'
        s.send(heloMessage.encode())

        # display response
        print(s.recv(1024).decode())

        # send MAIL FROM: <fake@fake.fr>
        mailFrom = 'MAIL FROM:' + fromAddress + '\r\n'
        s.send(mailFrom.encode())

        # display response
        print(s.recv(1024).decode())

        # send RCPT TO: <target@coolplace.org>
        mailTo = 'RCPT TO:' + toAddress + '\r\n'
        s.send(mailTo.encode())

        # display response
        print(s.recv(1024).decode())

        # send DATA
        data = 'DATA\r\n'
        s.send(data.encode())

        # display response
        # no matter what this seems to display the code: 354 End data with
        # <CR><LF>.<CR><LF>
        print(s.recv(1024).decode())

        # send message
        s.send((message + '\r\n.\r\n').encode())

        # display response
        print(s.recv(1024).decode())

        # send QUIT
        quit = 'QUIT\r\n'
        s.send(quit.encode())

        # display response
        print(s.recv(1024).decode())


def main():
        smtpServer = "128.143.2.9"
        port = "25"
        fromAddress = "atg5ad@virginia.edu"
        toAddress = "runkel@virginia.edu"
        message = ""
        line_count = 0
        with open('test2.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                        if line_count != 0:
                                fromAddress = "atg5ad@virginia.edu"
                                toAddress = row["email"]
                                message = """SUBJECT: Jefferson Society Interview Week
Dear """ + row["name"] + "," +"""

The Jefferson Society is conducting interviews this week for our Spring class. """ + row["reccer"] + """ recommended you come out to interview with us this semester. We're a speech and debate club--with little formal speech or debate structure. All of our subjects are proposed by our membership, and they range from the fictional to the philosophical. We encourage all to interview, no speaking experience needed. The interview lasts 30-45 minutes and will cover ideas, arguments, or topics you choose. Our members will try to draw out your thinking process, curiosity, and speaking style to gain a better understanding of how you could gain from joining us this Spring.
We encourage you to fill out a card online in advance of your interview at jeffsoc.blog, but there is no need to do so--you can show up and handwrite one if you desire. In an effort to be more transparent we are including important characteristics of a passing interview on our website. The most important part is the topics for discussion, which is where you can pick anything you would be comfortable engaging in a lively conversation and debate about. Generally, anything will go, so pick what you’re passionate about.

Interviews and other informative events will take place at Jefferson Hall, Hotel C on West Range, during the interview times (listed below) on any given day and we will get you a panel as soon as possible.

Interview Times
Tuesday January 22nd: 12PM-5PM & 7PM-9PM
Wednesday January 23rd: 10AM-5PM
Thursday January 24th: 12PM-5PM & 7PM-9PM
Friday January 25th: 10AM-5PM

You also are welcome to join us for these events:
Thursday January 24th: Hot Chocolate Reception; 6PM-7PM
Friday January 25th: Open House Meeting; 7:29PM

Please feel free to contact us at membership.chair@jeffersonsociety.org. We hope to see you there!

Regards,
Alex

Membership Chair
JLDS | Spring 2019

p.s. If you received this email as well as that asking you to interview again, we're sorry we couldn't fit into one email!
"""
                                sendMessage(
    smtpServer, port, fromAddress, toAddress, message)
                                print(    "email sent to: ",    row["name"],    "(",    row["email"],    ")",    "recc'd by ",     row["reccer"])
                        line_count += 1
        print("done")


if __name__ == "__main__":
        main()

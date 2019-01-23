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
    fromAddress = "president@whitehouse.gov"
    toAddress = "ro@virginia.edu"
    message = ""
    line_count = 0
    with open('test.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if line_count != 0:

                fromAddress = "president@jeffersonsociety.org"
                toAddress = row["computing_id"] + "@virginia.edu"
                message = """SUBJECT: Jefferson Society Interview Week

Hello """ + row["first"] + " " + row["last"] + " ,"
                if len(row["Num_ask_backs"]) > 0:
                    message += """

""" + row["Num_ask_backs"] + """ of your interviewers made a note that they enjoyed your interview and were hoping that you would interview again for the society. Please checkout the interview week Facebook Event for more information! We hope to see you soon.

Cheers,
The Jefferson Society"""
                else:
                    message += """

We enjoyed your interview with the Jefferson Society. Although we were unable to offer you admission at the time, we were hoping that you would interview again! Please checkout the interview week Facebook Event for more information! We hope to see you soon.

Cheers,
The Jefferson Society"""
                print(
                    "first:",
                    row["first"],
                    ", last:",
                    row["last"],
                    ", computing_id:",
                    row["computing_id"],
                    ", number of ask backs:",
                    row["Num_ask_backs"])
            line_count += 1
            sendMessage(smtpServer, port, fromAddress, toAddress, message)
    print("done")


if __name__ == "__main__":
    main()

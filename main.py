#!/usr/bin/python3
import sys
import imaplib
from imapclient import IMAPClient
from socket import gethostbyname, gaierror, create_connection
import email
from email import policy
from email.parser import BytesParser



## Conection
### If using gmail remember to enable insecure apps https://support.google.com/accounts/answer/6010255?hl=en
SERVER="imap.gmail.com"
USERNAME="pablohn6@gmail.com"
PASSWORD=""
MAILBOX="INBOX"
PROVIDER=""
WORD=""
try:
    gethostbyname(SERVER)
    #TODO: connect to port 993
except gaierror as e:
    print('invalid server: '+SERVER)
    print(str(e))
    sys.exit()

server = IMAPClient(SERVER, use_uid=True)

try:
    server.login(USERNAME,PASSWORD)
except imaplib.IMAP4.error as e:
    print('invalid credentials')
    print("Username: "+USERNAME)
    print("Password: "+PASSWORD)
    print(str(e))
    server.logout()
    sys.exit()


## Reading emails
### Folder select
try:
    server.select_folder(MAILBOX)
except imaplib.IMAP4.error as e:
    print("Unknown Mailbox: "+MAILBOX)
    print(str(e))
    server.logout()
    sys.exit()

### Reading emails
messages = server.search(['FROM', PROVIDER])
print("%d messages found" % len(messages))

for msgid, data in server.fetch(messages, ['RFC822', 'BODY[TEXT]','ENVELOPE']).items():
    envelope = data[b'ENVELOPE']
    body = data[b'BODY[TEXT]']
    print('ID #%d: "%s" received %s' % (msgid, envelope.subject.decode(), envelope.date))
    if WORD in envelope.subject.decode():
        print("email found id: "+str(msgid)+"\nmessage_id="+str(envelope.message_id))
        email_message = email.message_from_bytes(data[b'RFC822'])
        print(msgid, email_message.get('From'), email_message.get('Subject'))
        if 'message-id' in email_message:
            print('Message-ID:', email_message['message-id'])
        print(body)
        ## TODO: extract just the HTML

server.logout()

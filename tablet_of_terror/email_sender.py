import smtplib, ssl

user = 'tabletofterror21@gmail.com'
password = 'casaescuela21'
port = 465
reciever = 'floriskools1@hotmail.com'

message = """\
subject: TABLET OF TERROR

Laat je likken
"""
context = ssl.create_default_context()

for _ in range(5):
    print('sending email...')
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(user,password)
        server.sendmail(user,reciever,message)
    print('email sent!')
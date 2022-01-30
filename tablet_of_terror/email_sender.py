import smtplib, ssl


def send_email(opdracht='Enter message',gebruiker='dylano'):
    user = 'tot@dylano.me'
    password = 'Kankerenporno'
    smtp_adres = 'mail.antagonist.nl'    
    
    #override variables if gmail is passed
    if gebruiker == 'gmail':
        user = 'tabletofterror21@gmail.com'
        password = 'casaescuela21'
        smtp_adres = 'smtp.gmail.com'
    
    
    port = 465
    reciever = 'tabletofterror21@gmail.com'

    context = ssl.create_default_context()

    
    message = "\r\n".join([
  "From: tabletofterror21@gmail.com",
  "To: tabletofterror21@gmail.com",
  "Subject: TABLET OF TERROR",
  "",
  opdracht
  ])

    print('sending email...')
    with smtplib.SMTP_SSL(smtp_adres, port, context=context) as server:
        server.login(user,password)
        server.sendmail(user,reciever,message)
    print('email sent!')

# send_email(gebruiker='gmail')
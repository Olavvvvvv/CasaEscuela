import smtplib, ssl
def send_email(message_to_send):
    user = 'tabletofterror21@gmail.com'
    password = 'casaescuela21'
    port = 465
    reciever = 'tot@dylano.me'
    message_header = """/
    subject: TABLET OF TERROR
    
    Ok gasten,\n
    """
    message = message_header + message_to_send

    context = ssl.create_default_context()


    print('sending email...')
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(user,password)
        server.sendmail(user,reciever,message)
    print('email sent!')
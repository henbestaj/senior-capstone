import yagmail

yag = yagmail.SMTP('terrapintrackercontact@gmail.com', oauth2_file = './client_secret_145697339555-diqqlc1qtg0bc4q9ur10tjlc73a951bu.apps.googleusercontent.com.json')

to = 'henbestaj@gmail.com'
subject = 'Test'
body = 'Test'

yag.send(to = to, subject = subject, contents = body)
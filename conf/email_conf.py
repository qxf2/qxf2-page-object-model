#Details needed for the Gmail
#Fill out the email details over here
imaphost="imap.gmail.com"  #Add imap hostname of your email client
username="Add your email address or username here"

#Login has to use the app password because of Gmail security configuration
# 1. Setup 2 factor authentication
# 2. Follow the 2 factor authentication setup wizard to enable an app password
#Src: https://support.google.com/accounts/answer/185839?hl=en
#Src: https://support.google.com/mail/answer/185833?hl=en
app_password="Add app password here"

#Details for sending pytest report
smtp_ssl_host = 'smtp.gmail.com'  # Add smtp ssl host of your email client
smtp_ssl_port = 465  # Add smtp ssl port number of your email client
sender = 'abc@xyz.com' #Add senders email address here
targets = ['asd@xyz.com','qwe@xyz.com'] # Add recipients email address in a list





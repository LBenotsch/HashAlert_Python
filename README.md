# HashAlert_Python
An email alert application for EthOS distro.

There really wasn't an effective way to recieve alerts if a miner went down via EthOS. So I wrote this app to solve my issue, as well as for others. Feel free to use, re-distribute, or make changes.

# Linux Instructions
Run by using:
```
python HashAlert.py
```

# Configuration
The first method send_email() contains varaibles for email configuration.
```
fromaddr = ''  # Email address the application will send alerts through.
toaddrs = ''  # Email address to recieve alerts. Can setup multiple using a list.
username = ''  # Email account name. Usually the same as 'fromaddr'
password = ''  # Password for the Email account.
server = smtplib.SMTP('smtp.gmail.com:587')  # Server for the 'fromaddr' Email address (defualt is gmail).
```

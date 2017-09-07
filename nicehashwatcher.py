import sys

MIN_PROD_TRIGGER = 0.0030

class NotificationState:
  def __init__(self):
    self.isGood = True

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user

    header = 'To:' + recipient + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: ' + subject + '\n'
    print(header)
    msg = header + '\n' + body + '\n\n'
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.ehlo()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, recipient, msg)
    server.close()
    print('successfully sent the mail')


def check_nh(state):
    import subprocess
    try:
        print('Miner address:' + sys.argv[1])
        result = subprocess.run(args=['./phantomjs', 'nh.js', sys.argv[1]], stdout=subprocess.PIPE)
        ret = result.stdout.replace(b'\n', b' ').replace(b'\r', b'')
        import re
        p = re.compile(b"Profitability(.*?)BTC\/day")
        mr = p.search(ret).group(1).strip()
        print(mr)
        mrp = float(mr)
        print(mrp)
        if (mrp < MIN_PROD_TRIGGER):
            if (state.isGood == True):
                send_email(sys.argv[2], sys.argv[3], sys.argv[4], 'Nicehash is sad at ' + str(mrp),
                           'https://new.nicehash.com/miner/1FaZZ7QkTer2YsFQjRTCvVhrcNwJk8EMbg\n' + 'Current profitabiity: ' +  str(mrp) + '\n')
                state.isGood = False
        elif(state.isGood == False):
            state.isGood = True
    except:
        pass

import time
state = NotificationState()

while True:
    check_nh(state)
    time.sleep(60)

import pytz
import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import slack


slack_token = 'xoxp-50721412707-423273434950-738022195271-f31112d95bdab642fabf5c35a923a8b4'
slack_channel = '#email-watcher'
slack_user_name = 'Mearaf Tadewos'
mmcy_receiver = 'supporterinfo@mancityethiopia.com'
orgBaseUrl = 'https://mmcytech.com'
organizationName = 'MMCY TECH'
client = slack.WebClient(token=slack_token)
chnl = slack_channel


msg_template = """Hi, {name}!
We are checking up your email account to track downtime.
Thank you for working with us!
{website}.
"""
monitor_msg_template = """ Hello!
I sent test email to: {receiver} at: {time} in New York time zone and got the STATUS: {status}.
Full status object is: {msgObj}
Thank you for working with us.
{website}.
"""

slack_info = """ Alert! (Now the test must be working.)
I just sent test email to: {receiver} at: {time} in New York time zone and It wasn't delivered. 
I got the STATUS: {_status}.
Full report object is: {_alert_msg}
Company: {org_url}.
"""
Bot_User_OAth_Token = 'xoxb-50721412707-2204438718998-mpjpi70cidASiCDOzzwnROfP'


def alert_slack(_status, _alert_msg):
    device: 'myLinux device'
    ip: 'test ip address'
    ny_tz = pytz.timezone('America/New_York')
    datetime.now(ny_tz)
    time_stamp = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    message = format_slack_msg(time_stamp, _status, _alert_msg)
    try:
        client = slack.WebClient(token='xoxb-50721412707-2204438718998-mpjpi70cidASiCDOzzwnROfP')
        client.chat_postMessage(channel='email-watcher', text=message)
        sent_to_slack = True
        print("JUST SENT AN ALERT MESSAGE TO SLACK. STATUS IS: ", sent_to_slack)
    except:
        sent_to_slack = False
        print("FAILED TO SEND ALERT MESSAGE TO SLACK. STATUS IS: ", sent_to_slack)


def format_msg(_name="Test Email Account", _website="https://mmcytech.com"):
    _msg = msg_template.format(name=_name, website=_website)
    return _msg


ntz = pytz.timezone('America/New_York')


def format_slack_msg(_time, _status, _alert_msg):
    slack_alert_msg = slack_info.format(receiver=mmcy_receiver, time=_time, _status=_status, _alert_msg=_alert_msg, org_url=orgBaseUrl)
    return slack_alert_msg


def format_monitor_msg(_time, _status, _msgObj):
    monitor_msg = monitor_msg_template.format(receiver=mmcy_receiver, time=_time, status=_status, msgObj=_msgObj,
                                              website=orgBaseUrl)
    return monitor_msg


def send(_name, to_email=None, _status=False):
    msg = format_msg(_name=_name)
    try:
        send_mail(text=msg, to_emails=[to_email], html=None)
        _status = True
    except:
        _status = False
    return _status


def responseSender(receiver, _monitor_msg, _status):
    sent = False
    ntz = pytz.timezone('America/New_York')
    datetime.now(ntz)
    time_stamp = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    message = format_monitor_msg(time_stamp, _status, _monitor_msg)
    try:
        send_mail(text=message, to_emails=[receiver], html=None)
        sent = True
    except:
        sent: False
    return sent


def send_mail(text='Email Body', subject='Email downtime checking.',
              from_email='MMCY-TECH | MAIL STANDBY<mailstandbymmcytech@gmail.com>', to_emails='test@mmcytech.com',
              html=None):
    username = 'mailstandbymmcytech@gmail.com'
    password = 'mailstandbymmcytech@gmail.com2021'
    assert isinstance(to_emails, list)
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)
    if html != None:
        html_part = MIMEText(html, 'html')
        msg.attach(html_part)
    msg_str = msg.as_string()
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()


if __name__ == "__main__":
    name = "Test Email Address"
    _username = 'mailstandbymmcytech@gmail.com'
    email_addr = 'supporterinfo@mancityethiopia.com'
    tz = pytz.timezone('America/New_York')
    isSent = False
    dateTimeObj = datetime.now(tz)
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    print("PROCESS STARTED AT: ", timestampStr)
    print("-------------------------SENDING EMAIL TO @mmcytech.com ACCOUNT---------------------")
    print("RECEIVER EMAIL ADDRESS: ", email_addr)
    dateTimeObj = datetime.now(tz)
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    isSent = send(name, to_email=email_addr, _status=True)
    print('EMAIL SENT TO THE RECEIVER: ', isSent)
    print(timestampStr)
    print("-------------------------RUNNING EMAIL NOTIFICATION TO MONITOR EMAIL---------------------")
    admin_msg = {
        'recipient': email_addr,
        'status': isSent,
        'time_stamp': timestampStr
    }
    print(timestampStr)
    status = isSent
    dateTimeObj = datetime.now(tz)
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    res = responseSender(_username, admin_msg, isSent)
    print('NOTIFICATION SENT TO THE MONITOR EMAIL: ', res)
    if not isSent:
        print("-------------------------EXECUTING SLACK NOTIFICATION ---------------------")
        dateTimeObj = datetime.now(tz)
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        alert_slack(isSent, admin_msg)
        print(timestampStr)

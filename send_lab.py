import os
import time
import configparser
import json
import smtplib
import mimetypes
import base64

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from datetime import datetime, timezone

def last_change_time(path):
    m_time = os.path.getmtime(path)
    data_time = datetime.fromtimestamp(m_time).strftime("%d-%m-%Y %H:%M:%S")
    return str(data_time)

def get_file_info(path, file):
    root = str(path[0])
    dir = str(path[1]) if path[1] else '\\'
    file_name = str(file)

    file_path = root + dir + file_name
    last_change = last_change_time(file_path)

    return (file_path, last_change)

def key_time(file):
    return file[1]

def items_checking(dict):
    selected_items = list(map(int, input("Отправить лабы: ").split()))

    out_of_range_items = set(selected_items).difference(set(dict.keys()))
    if  out_of_range_items != set():
        print(f"№ {out_of_range_items} не существует\n")
        return False
    else:
        return selected_items

def file_selection(content):
    file_match = {}

    for index, i in enumerate(content):
        file_match[index] = i[0]
        print(f"{index}.\t{i[0]}\n\t{i[1]}\n")

    items = False
    while items is False:
        items = items_checking(file_match)

    return items, file_match

def match_teacher(discipline):
    dict ={
        'веб': 'Poryev',
        'розподілене_обчисл': 'Poryev',
        'спас': 'Kovtun',
        'экономика': 'Fedorenko',
        'якість_та_тестування': 'Tkachenko'
    }

    return str(dict[discipline])

def message_content(i, config):
    file_name = lab_number_dict[i]
    teacher = match_teacher(file_name.split('\\')[1])
    email = config[teacher]['email']
    topic = file_name.split('\\')[2][:-4]

    return {
        'file_name': file_name,
        'teacher': teacher,
        'email': email,
        'topic': topic
    }


def create_message_with_attachment(
    sender, to, subject, message_text, file):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(file, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(file, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(file, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(file, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string())}


def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print ('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print (f'An error occurred: {error}')


config = configparser.ConfigParser()
config.read("config.ini")
with open('credentials.json') as json_file:
    api_data = json.load(json_file)

me = config['Me']
client_id = api_data['installed']['client_id']
project_id = api_data['installed']['project_id']
auth_uri = api_data['installed']['auth_uri']
token_uri = api_data['installed']['token_uri']
auth_provider_x509_cert_url = api_data['installed']['auth_provider_x509_cert_url']
client_secret = api_data['installed']['client_secret']
redirect_uris = api_data['installed']['redirect_uris']







# content = [(root, dir, file) for root, dir, file in os.walk(".") if '1semestr' not in root] #indexing all files
# content = sorted([get_file_info(path, file) for path in content for file in path[2] if '.pdf' in file], #filtering pdf and adding last change time sorting
#                  key=key_time, reverse=True)


#
# labs_to_send, lab_number_dict = file_selection(content) #number of labs, mathcing numbers with filenames
#
# messages = [message_content(i, config) for i in labs_to_send] #list of dicts with message info


# messages_to_send = [create_message_with_attachment(
#     sender=me, to=i['email'], subject=i['topic'], message_text='', file=i['file_name'])
#     for i in messages]


x = create_message_with_attachment(sender=me, to='', subject='', message_text='', file='.\\спас\\лаб1\\СПАС_ІПЗ-31_лаб1_Якімечко.pdf')

print(x)












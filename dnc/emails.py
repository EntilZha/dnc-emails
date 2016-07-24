import email
from functional import pseq
import requests


def save_email(email_id, url):
    r = requests.get(url)
    if r.status_code != 200:
        print('Error occurred at id={id}'.format(id=email_id))
        return False
    with open('data/{id}.txt'.format(id=email_id), 'w') as f:
        f.write(r.text)
    return True


def save_all_emails(start=1, stop=22456):
    base_url = 'https://wikileaks.org/dnc-emails/get/{id}'
    urls = [(i, base_url.format(id=i)) for i in range(start, stop + 1)]
    pseq(urls).map(
        lambda kv: (kv[0], kv[1], save_email(kv[0], kv[1]))
    ).to_json('data/results.json')


def parse_email(path):
    with open(path) as f:
        email_message = email.message_from_file(f)
    body = ""

    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))

            if content_type == 'text/plain' and 'attachment' not in content_disposition:
                body = part.get_payload(decode=True)
                break
    else:
        body = email_message.get_payload(decode=True)

    if isinstance(body, bytes):
        return {
            'from': email_message['from'],
            'to': email_message['to'],
            'body': body.decode('utf-8')
        }
    else:
        return {
            'from': email_message['from'],
            'to': email_message['to'],
            'body': body
        }

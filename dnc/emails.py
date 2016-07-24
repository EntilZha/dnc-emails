import email
from functional import pseq
import requests


START_ID = 1
STOP_ID = 22456


def save_email(email_id, url):
    r = requests.get(url)
    if r.status_code != 200:
        print('Error occurred at id={id}'.format(id=email_id))
        return False
    with open('data/{id}.txt'.format(id=email_id), 'w') as f:
        f.write(r.text)
    return True


def save_all_emails(start=START_ID, stop=STOP_ID):
    base_url = 'https://wikileaks.org/dnc-emails/get/{id}'
    urls = [(i, base_url.format(id=i)) for i in range(start, stop + 1)]
    pseq(urls).map(
        lambda kv: (kv[0], kv[1], save_email(kv[0], kv[1]))
    ).to_json('data/results.json')


def parse_email_body(email_message):
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))

            if content_type == 'text/plain' and 'attachment' not in content_disposition:
                return part.get_payload(decode=True)
    else:
        return email_message.get_payload(decode=True)
    return ""


def parse_email(path):
    with open(path) as f:
        email_message = email.message_from_file(f)
    raw_body = parse_email_body(email_message)

    if isinstance(raw_body, bytes):
        try:
            body = raw_body.decode('utf-8')
        except UnicodeDecodeError:
            try:
                body = raw_body.decode('windows-1252')
            except UnicodeDecodeError:
                print("Could not parse: {0}".format(path))
                raise
    else:
        body = raw_body
    return {
        'from': email_message['from'],
        'to': email_message['to'],
        'body': body
    }


def parse_all_emails(start=START_ID, stop=STOP_ID):
    base_path = 'data/{id}.txt'
    pseq.range(start, stop + 1)\
        .map(lambda i: parse_email(base_path.format(id=i)))\
        .to_jsonl('emails.jsonl')

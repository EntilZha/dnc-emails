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

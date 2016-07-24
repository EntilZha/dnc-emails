from functional import pseq
import requests


def save_email(url):
    r = requests.get(url)
    if r.status_code != 200:
        print('Error occurred at id={id}'.format(id=id))
        return False
    with open('data/{id}.txt'.format(id=id), 'w') as f:
        f.write(r.text)
    return True


def save_all_emails(start=1, stop=22456):
    base_url = 'https://wikileaks.org/dnc-emails/get/{id}'
    urls = [base_url.format(id=i) for i in range(start, stop + 1)]
    pseq.range(urls).map(lambda url: (url, save_email(url))).to_json('data/results.json')

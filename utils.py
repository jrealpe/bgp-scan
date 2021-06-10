import re

def encode2ascii(raw):
    return raw.encode('ascii')


def decode2ascii(raw):
    return raw.decode('ascii')


def tokenizer(data):
    raw = re.sub(r'[ ]{3,}', '', data)
    raw = ' | '.join([_.strip() for _ in raw.split('\r\n')])
    return raw.strip()

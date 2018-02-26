#!/usr/bin/env python

# Takes a tokens.xml file from FreeOTP (Android App) and outputs
# One-Time-Passwords generated with `oathtool`.

from base64 import b16decode, b32encode
import xmltodict
import os
import json

token_filename = os.path.dirname(os.path.realpath(__file__)) + '/tokens.xml'

with open(token_filename, 'r') as token_file:
    data = xmltodict.parse(token_file.read().replace('&quot;', '"'))

accs = data['map'].values()

def to_hex(val, nbits):
    return '{:02X}'.format((val + (1 << nbits)) % (1 << nbits))

otps = {}

for acc in list(data['map'].values())[0]:
    if acc['@name'] == 'tokenOrder': continue

    info = json.loads(acc['#text'])
    print(info['secret'][0], to_hex(info['secret'][0], 8))
    secret = ''.join([to_hex(x, 8) for x in info['secret']])

    otps[acc['@name']] = os.popen(
        'oathtool --base32 --totp={algo} --digits={digits} --time-step-size={period}s {secret}'.format(
            algo = info['algo'].lower(),
            digits = info['digits'],
            period = info['period'],
            secret = b32encode(b16decode(secret)).decode()
        )
    ).read().strip()

# print the passwords to stdout
for name, otp in otps.items():
    print("{}: {}".format(name, otp))

# show a notification
# requires python-gobject
from gi import require_version
require_version('Notify', '0.7')
from gi.repository import Notify
Notify.init('OTP')
Notify.Notification.new(
    'One-Time-Passwords',
    '\n'.join(['{}: {}'.format(name.split(':')[0], otp) for name, otp in otps.items()])
).show()

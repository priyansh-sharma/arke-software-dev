import imaplib
import email
import re
mail = imaplib.IMAP4_SSL('imap.gmail.com')
# imaplib module implements connection based on IMAPv4 protocol
mail.login('ps06271999@@gmail.com', 'atlasaeronautics')
# >> ('OK', [username at gmail.com Vineet authenticated (Success)'])
mail.select('inbox') # Connected to inbox.
result, data = mail.uid('search', None, "ALL")
# search and return uids instead
i = len(data[0].split()) # data[0] is a space separate string
for x in range(i):
    latest_email_uid = data[0].split()[x] # unique ids wrt label selected
    result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    # fetch the email body (RFC822) for the given ID
    raw_email = email_data[0][1]
    # continue inside the same for loop as above
    raw_email_string = raw_email.decode('utf-8')
    # converts byte literal to string removing b''
    email_message = email.message_from_string(raw_email_string)
    # this will loop through all the available multiparts in mail
    for part in email_message.walk():
        if part.get_content_type() == "text/plain":  # ignore attachments/html
            body = part.get_payload(decode=True)
            save_string = str("emaildump" + str(x) + ".txt")
            # location on disk
            myfile = open(save_string, 'w')
            body = body.decode('utf-8')
            # for line in body.splitlines():
            #     if not line.startswith('<https'):
            #         myfile.write(line + "\n")
            myfile.write(body)
            # body is again a byte literal
            myfile.close()
        else:
            continue

# Get address from email dump

f = open("emaildump0.txt", 'r')
temp = ""
start = 0
for line in f:
    if line.startswith('ALRM'):
        start = 1
        continue
    if line.startswith('CrossStreet'):
        start = 0
        continue
    if (start == 1):
        temp += line

temp = temp.replace("\n", " ")



# Using Python requests and the Google Maps Geocoding API.

import requests

GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

params = {
    'address': temp,
    'sensor': 'false',
    'region': 'us'
}

# Do the request and get the response data
req = requests.get(GOOGLE_MAPS_API_URL, params=params)
res = req.json()

# Use the first result
result = res['results'][0]

geodata = dict()
geodata['lat'] = result['geometry']['location']['lat']
geodata['lng'] = result['geometry']['location']['lng']
geodata['address'] = result['formatted_address']

print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))
# 221B Baker Street, London, Greater London NW1 6XE, UK. (lat, lng) = (51.5237038, -0.1585531)

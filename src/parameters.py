import pprint
import json
import hashlib
import datetime

def formatData(values):
    username = values['-USER-']
    if username != '':
        username = username[:64]
    
    # Message
    message = values['-IN-']
    if message != '':
        message = [message[i:i+64] for i in range(0, len(message), 64)]
    return username, message

def createChatHash():
    # Create unique chat hash
    H = hashlib.sha3_512()
    H.update(b"An Unrestricted Decentralized Communications Platform")
    H.update(b"By")
    H.update(b"Logical Mechanism")
    chatHash = H.hexdigest()
    chatHash = chatHash[:64]
    return chatHash


def createChannelHash():
    H = hashlib.sha3_512()
    H.update(b"General Communications")
    H.update(b"By")
    H.update(b"Logical Mechanism")
    channelHash = H.hexdigest()
    channelHash = channelHash[:64]
    return channelHash

def createUserHash(username):
    H = hashlib.sha3_512()
    H.update(str.encode(username))
    H.update(b"By")
    H.update(b"Logical Mechanism")
    userHash = H.hexdigest()
    userHash = userHash[:64]
    return userHash

def create(username, message):
    # Create unique chat hash
    chatHash = createChatHash()
    # Create unique channel hash
    channelHash = createChannelHash()
    # Get user hash
    userHash = createUserHash(username)
    # Time Stamp the message
    timestamp = str(datetime.datetime.now(datetime.timezone.utc))
    timestamp = timestamp[:64]
    # Create the data object
    data = {}
    data['1337'] = {}
    data['1337']['1'] = chatHash
    data['1337']['2'] = channelHash
    data['1337']['3'] = timestamp
    data['1337']['4'] = userHash
    for i in range(len(message)):
        data['1337'][str(5+i)] = message[i]
    # data['1337']['5'] = message
    # Write to metadata.json
    with open('metadata.json', 'w+') as outfile:
        json.dump(data, outfile, indent=3)

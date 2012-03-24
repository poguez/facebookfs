import pycurl
import json
import cStringIO


# The application's token
#token = 'AAAEx8ZB2Y28EBAO8pd0f5HxneV14FIZBKea4XAjnVoY3ZBvZCA3zdUdIuksJ7uj4bOgZBGjs4kNlpDyzII0jmZAQWyAbhtIbKRSzjGDIGQsQZDZD'
token = 'AAAAAAITEghMBAIchZB6hG97BPZBJzvBcalVdhPe08L2umP5wzH0d97RCxv5mfBZCd2z7kZCrwwk82olIclqc0rZAdUZCZC7wpBCXo0ztF1X0QZDZD'

# Function that gets stuff (photos, albums, friends) from a certain user (whose)
def fetch(whose, what):    
    where = 'https://graph.facebook.com/' + whose +'/' + what + '?access_token=' + token
    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, str(where))
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()
    contents = json.loads(buf.getvalue())['data']
    buf.close()
    return contents

# Function that gets all of the pictures from a specific album 
def get_album_photos(album_id):
    url = 'https://graph.facebook.com/' + album_id + '/photos?access_token=' + token
    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, str(url))
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()
    contents = json.loads(buf.getvalue())['data']
    buf.close()
    return contents

# Fetch my complete friend list
# Don't bother with paging when getting the list of all your friends.
# You can get the whole list with one single request; paging here is useless.
my_friends = fetch('me', 'friends')

# Create a dictionary with all my friends and their IDs
friend_dictionary = {}
for friend in my_friends:
    friend_dictionary[friend['id']] = {'name':friend['name']}
print friend_dictionary

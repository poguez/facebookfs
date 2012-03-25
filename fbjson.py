import pycurl
import json
import cStringIO

# The application's token
#token = 'AAAEx8ZB2Y28EBAO8pd0f5HxneV14FIZBKea4XAjnVoY3ZBvZCA3zdUdIuksJ7uj4bOgZBGjs4kNlpDyzII0jmZAQWyAbhtIbKRSzjGDIGQsQZDZD'
#token = 'AAAAAAITEghMBAIchZB6hG97BPZBJzvBcalVdhPe08L2umP5wzH0d97RCxv5mfBZCd2z7kZCrwwk82olIclqc0rZAdUZCZC7wpBCXo0ztF1X0QZDZD'

token = ""
# Function that gets stuff (photos, albums, friends) from a certain user (whose)

def get_json_from_url(url):
    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.setopt(c.CONNECTTIMEOUT, 5)
    c.setopt(c.TIMEOUT, 8)
    c.perform()
    json_object = json.loads(buf.getvalue())
    return json_object

def fetch(whose, what):    
    url = 'https://graph.facebook.com/' + whose +'/' + what + '?access_token=' + token
    return get_json_from_url(url)

# Function that gets all of the pictures from a specific album 
def get_album_photos(album_id):
    url = 'https://graph.facebook.com/' + album_id + '/photos?access_token=' + token
    return get_json_from_url(url)


# Fetch my complete friend list
# Don't bother with paging when getting the list of all your friends.
# You can get the whole list with one single request; paging here is useless.
def get_my_friends():
    my_friends = fetch('me', 'friends') 
    my_friends = my_friends['data']
    # Create a dictionary with all my friends and their IDs
    friend_dictionary = {}
    for friend in my_friends:
        #friend_dictionary[friend['name']] = {'id': friend['id']}
        name = friend['name']
        name = name.encode('ascii', 'replace')
        id_number = friend['id']
        id_number = id_number.encode('ascii', 'replace')
        friend_dictionary[name] = []
    return friend_dictionary

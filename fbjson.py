import pycurl
import json
import cStringIO

# The application's token
token = ''

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

# Function that gets a specific object from a specific person
def fetch(whose, what):    
    url = 'https://graph.facebook.com/' + whose +'/' + what + '?access_token=' + token
    return get_json_from_url(url)

# Function that gets all of the pictures from a specific album 
def get_album_photos(album_id):
    url = 'https://graph.facebook.com/' + album_id + '/photos?access_token=' + token
    return get_json_from_url(url)

# Function that gets every album from a friend
def get_albums_from_friend(friend_id):
    album_list = []
    albums = fetch(friend_id, 'albums')['data']
    for album in albums:
        album['name'] = album['name'].encode('ascii', 'replace')
        album_list.append(album['name'])
    return album_list

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

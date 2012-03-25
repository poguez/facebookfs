import pycurl
import json
import cStringIO

# The application's token
token = 'AAAAAAITEghMBACDHmzfQkpQgO2lQDlsyJYBTL6pj7BhwCBhXKbh3Pe3cW6fapNkslwV3Qv8BBf52y8wy6MzOnAfZCGZA4CgEGLsflfoAZDZD'

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
    album_dictionary = {}
    albums = fetch(friend_id, 'albums')['data']
    for album in albums:
        name = album['name'].encode('ascii', 'replace')
        album_id = album['id'].encode('ascii','replace')
        album_dictionary[name] = {'id' : album_id }
    return album_dictionary

#Function that gets all videos from a friend
def get_videos_from_friend(friend_id):
    videos_dictionary = {}
    videos = fetch(friend_id, 'videos')['data']
    for video in videos:
        video_id = video['id'].encode('ascii', 'replace')
        name = video['name'].encode('ascii', 'replace')
        url = video['source'].encode('ascii')
        videos_dictionary[name] = { 'id' : video_id, 'url' : url }    
    return videos_dictionary

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
        friend_dictionary[name] = { "id": id_number } 
    return friend_dictionary

if __name__ == "__main__":
    print get_videos_from_friend('chavezgu')
    print get_albums_from_friend('noe.dominguez')

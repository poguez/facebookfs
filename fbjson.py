import json
import urllib

# The application's token

token = ""

# Function that gets stuff (photos, albums, friends) from a certain URL
def get_json_from_url(url):
    ret = urllib.urlopen(url)
    json_object = json.loads(ret.read())
    return json_object

# Function that gets a specific object in which a person has been tagged
#domain: [photos, videos]
def fetch(whose, what):    
    url = 'https://graph.facebook.com/' + whose +'/' + what + '?access_token=' + token
    return get_json_from_url(url)


# Function that gets all of the pictures from a specific album 
def get_album_photos(album_id):
    url = 'https://graph.facebook.com/' + album_id + '/photos?access_token=' + token
    photos = get_json_from_url(url)['data']
    photo_dictionary = {}
    counter = 1
    for photo in photos:
        photo_id = photo['id'].encode('ascii','replace')
        if 'name' in photo:
            photo_name = photo['name'].encode('ascii','replace')
        else:
            photo_name = 'unnamed' + str(counter)
            counter += 1
        photo_source = photo['source'].encode('ascii','replace')
        photo_dictionary[photo_id + ".jpg"] = {'name' : photo_name ,'source' : photo_source}
    return photo_dictionary



# Function that gets every album from a friend
def get_albums_from_user(user_id):
    album_list = []
    albums = fetch(user_id, 'albums')['data']
    for album in albums:
        name = album['name'].encode('ascii', 'replace')
        album_id = album['id'].encode('ascii','replace')
        album_list.append(name + '_' + album_id)
    return album_list

# Function that gets all videos where my friend is present
def get_videos_from_user(user_id):
    videos_dictionary = {}

    # Get the videos where my friend has been tagged
    videos_tagged = fetch(user_id, 'videos')['data']
    counter = 1
    for video in videos_tagged:
        video_id = video['id'].encode('ascii', 'replace')
        if 'name' in video:
            video_name = video['name'].encode('ascii', 'replace')
        else:
            video_name = 'unnamed' + str(counter)
            counter += 1
        url = video['source'].encode('ascii')
        videos_dictionary[video_id] = { 'name' : video_name, 'url' : url }

    # Get the videos my friend has uploaded
    videos_uploaded = fetch(user_id, "videos/uploaded")['data']
    counter = 1
    for video in videos_uploaded:
        video_id = video['id'].encode('ascii', 'replace')
        if 'name' in video:
            video_name = video['name'].encode('ascii', 'replace')
        else:
            vide_name = 'unnamed' + str(counter)
            counter += 1
        url = video['source'].encode('ascii')
        videos_dictionary[video_id] = { 'name' : video_name, 'url' : url }    
    return videos_dictionary

# Fetch my complete friend list
# Don't bother with paging when getting the list of all your friends.
# You can get the whole list with one single request; paging here is useless.
def get_my_friends():
    my_friends = fetch('me', 'friends')['data']
    # Create a dictionary with all my friends and their IDs
    friend_list = []
    for friend in my_friends:
        name = friend['name'].encode('ascii', 'replace')
        id_number = friend['id'].encode('ascii', 'replace')
        friend_list.append(name + '_' + id_number) 
    return friend_list


import os
import urllib

def create_ff(temp_folder, path):
    """ Create friend folder and album """
    folder = temp_folder
    # We need 4 because of the path structure: [folder, friend, photos, album]
    # This WON'T work with videos!
    for i in range(len(path)):
        folder += ('/' + path[i])

    if(not os.path.exists(folder)):
        os.makedirs(folder)

    return folder



def get_photos(photos, folder):
    album_photos = {}
    for (photo_id, value) in photos.iteritems():
        abs_path_foto = folder + '/' + photo_id
        if(not os.path.exists(abs_path_foto)):
            urllib.urlretrieve(value['source'], abs_path_foto)
        image_file = open(abs_path_foto, "r")
        image_file.seek(0)
        size = os.path.getsize(abs_path_foto)
        album_photos[photo_id] = image_file.read(size)

    return album_photos

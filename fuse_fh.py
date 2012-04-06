import os
import urllib

def get_photos(photos, folder):
    album_photos = {}
    for (photo_id, value) in photos.iteritems():
        abs_path_foto = folder + '/' + photo_id
        urllib.urlretrieve(value['source'], abs_path_foto)
        image_file = open(abs_path_foto, "r")
        image_file.seek(0)
        size = os.path.getsize(abs_path_foto)
        album_photos[photo_id] = image_file.read(size)

    return album_photos

#!/usr/bin/env python2

#
# CupsFS.py: a FUSE filesystem for mounting an LDAP directory in Python
# Need python-fuse bindings, and an LDAP server.
# usage: ./CupsFS.py <mountpoint>
# unmount with fusermount -u <mountpoint>
#

import stat
import errno
import fuse
import os
from time import time
from subprocess import *
import fbjson
import urllib
import tempfile

fuse.fuse_python_api = (0, 2)

home_folder = os.getenv('HOME') + '/fbfotos'

class MyStat(fuse.Stat):
  def __init__(self):
      self.st_mode = stat.S_IFDIR | 0755
      self.st_ino = 0
      self.st_dev = 0
      self.st_nlink = 2
      self.st_uid = os.geteuid()
      self.st_gid = os.getgid()
      self.st_size = 4096
      self.st_atime = 0
      self.st_mtime = 0
      self.st_ctime = 0

class FacebookFS(fuse.Fuse):
  def __init__(self, *args, **kw):
      fuse.Fuse.__init__(self, *args, **kw)

      # Get our list of printers available.

    
      self.friends = fbjson.get_my_friends()
      self.photos = {}
      self.videos = {}
      self.temp_folder = tempfile.mkdtemp(prefix="fbfs")
      self.curr_alb_photos = {}
      #self.friends = { "Noe Dominguez": [], "Everardo Padilla": [] }
      #self.printers = {"biblio1": [], "biblio2": []}
      #self.files = { "photos" : [], "videos" : [] }
      #self.lastfiles = { "1" : "Hola", "2":"Mundo"}

  def getattr(self, path):
      st = MyStat()
      pe = path.split('/')[1:]

      st.st_atime = int(time())
      st.st_mtime = st.st_atime
      st.st_ctime = st.st_atime
      if path == '/':
          pass
      #elif self.friends.has_key(pe[-1]):
          #pass
      elif len(pe) == 4:
          st = os.stat(self.temp_folder + '/' + pe[3])
      #else:
          #return -errno.ENOENT
      return st

  def readdir(self, path, offset):
      dirents = [ '.', '..' ]
      path_separeted = path[1:].split("/")
      #names_of_friends = []
      files_to_retrieve = ["photos" , "videos"]
      #for key, value in self.friends.iteritems():
          #names_of_friends.append(value['name'])

      if path == '/':
          #dirents.extend(names_of_friends)
          dirents.extend(self.friends)

      elif path[1:] in self.friends:
          dirents.extend(files_to_retrieve)
          #dirents.extend(self.friends[path[1:]]['folders'])

      elif path_separeted[-1] == 'photos':
          album_id = path_separeted[-2].split("_")[1]
          albums = fbjson.get_albums_from_user(album_id)
          dirents.extend(albums)

      # Inside an album!
      elif path_separeted[-2] == 'photos':
          album_id = path_separeted[-1].split("_")[1]
          self.photos = fbjson.get_album_photos(album_id)
          for (photo_id, value) in self.photos.iteritems():
            abs_path_foto = self.temp_folder + '/' + photo_id
            urllib.urlretrieve(value['source'], abs_path_foto)
            image_file = open(abs_path_foto, "r")
            image_file.seek(0)
            size = os.path.getsize(abs_path_foto)
            self.curr_alb_photos[photo_id] = image_file.read(size)
          dirents.extend(self.photos.keys())

      # Inside videos!
      elif path_separeted[-1] == 'videos':
          user_id = path_separeted[-2].split("_")[1]
          self.videos = fbjson.get_videos_from_user(user_id)
          dirents.extend(self.videos.keys())

      for r in dirents:
          yield fuse.Direntry(r)

  def mknod(self, path, mode, dev):
      #pe = path.split('/')[1:] # Path elements 0 = printer 1 = file
      #image_id = pe[-1]
      #self.photos[image_id] = { "name":"name", "source":"url" }
      #self.files[pe[1]] = ""
      #self.lastfiles[pe[1]] = ""
      return 0

  def unlink(self, path):
      #pe = path.split('/')[1:] # Path elements 0 = printer 1 = file
      #self.printers[pe[0]].remove(pe[1])
      #del(self.files[pe[1]])
      #del(self.lastfiles[pe[1]])
      return 0

  def read(self, path, size, offset):
      pe = path.split('/')[1:] # Path elements 0 = printer 1 = file
      #if(pe[-1] == "videos"):
          #video_id = pe[-1]
          #video = self.videos.get(image_id)
          #urllib.urlretrieve(video['source'], os.getenv('HOME') + '/' + video_id)
          #video_file = open(os.getenv('HOME') + '/' + video_id, "rb")
          #video_file.seek(offset)
          #size = os.path.get_size(video_file)
          #return video_file.read(size)
      #else:
          #image_id = pe[-1]
          #image = self.photos.get(image_id)
          ##dire_path = self.create_dir(path[:-len(pe[-1])])
          #urllib.urlretrieve(image['source'], os.getenv('HOME') + '/' + image_id)
          #image_file = open(os.getenv('HOME') + '/' + image_id, "rb")
          #image_file.seek(offset)
          #size = os.path.get_size(image_file)
          #return image_file.read(size)

      #return self.files[pe[1]][offset:offset+size]
      return 0

  def write(self, path, buf, offset):
      #pe = path.split('/')[1:] # Path elements 0 = printer 1 = file
      #image_id = pe[-1]
      #image = self.photos.get(image_id)
      ##self.photos[pe[1]] += buf
      #return len(buf)
      return 0

  def release(self, path, flags):
      #pe = path.split('/')[1:] # Path elements 0 = printer 1 = file
      #if len(self.files[pe[1]]) > 0:
          #lpr = Popen(['lpr -P ' + pe[0]], shell=True, stdin=PIPE)
          #lpr.communicate(input=self.files[pe[2]])
          #lpr.wait()
          #self.lastfiles[pe[1]] = self.files[pe[1]]
          #self.files[pe[1]] = "" # Clear out string
      return 0

  def open(self, path, flags):
      return 0

  def truncate(self, path, size):
      return 0

  def utime(self, path, times):
      return 0

  def mkdir(self, path, mode):
      return 0

  def rmdir(self, path):
      return 0

  def rename(self, pathfrom, pathto):
      return 0

  def fsync(self, path, isfsyncfile):
      return 0

  def create_dir(self, dire):
      if(not os.path.exists(dire)):
          os.makedirs(home_folder + dire)
      return home_folder + dire + "/"



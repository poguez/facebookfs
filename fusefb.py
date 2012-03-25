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

fuse.fuse_python_api = (0, 2)

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
      #self.friends = { "Noe Dominguez": [], "Everardo Padilla": [] }


      #self.printers = {"biblio1": [], "biblio2": []}
      #self.files = { "1" : "Hola", "2":"Mundo"}
      #self.lastfiles = { "1" : "Hola", "2":"Mundo"}

  def getattr(self, path):
      st = MyStat()
      pe = path.split('/')[1:]

      st.st_atime = int(time())
      st.st_mtime = st.st_atime
      st.st_ctime = st.st_atime
      if path == '/':
          pass
      elif self.friends.has_key(pe[-1]):
          pass
      #elif self.lastfiles.has_key(pe[-1]):
          #st.st_mode = stat.S_IFREG | 0666
          #st.st_nlink = 1
          #st.st_size = len(self.lastfiles[pe[-1]])
      else:
          return -errno.ENOENT
      return st

  def readdir(self, path, offset):
      dirents = [ '.', '..' ]
      if path == '/':
          dirents.extend(self.friends.keys())
          #dirents.extend(self.friends.keys())
      #else:
          #dirents.extend(self.friends[path[1:]])
      for r in dirents:
          yield fuse.Direntry(r)

  def mknod(self, path, mode, dev):
      #pe = path.split('/')[1:]        # Path elements 0 = printer 1 = file
      #self.printers[pe[0]].append(pe[1])
      #self.files[pe[1]] = ""
      #self.lastfiles[pe[1]] = ""
      return 0

  def unlink(self, path):
      #pe = path.split('/')[1:]        # Path elements 0 = printer 1 = file
      #self.printers[pe[0]].remove(pe[1])
      #del(self.files[pe[1]])
      #del(self.lastfiles[pe[1]])
      return 0

  def read(self, path, size, offset):
      #pe = path.split('/')[1:]        # Path elements 0 = printer 1 = file
      #return self.lastfiles[pe[1]][offset:offset+size]
      return 0

  def write(self, path, buf, offset):
      #pe = path.split('/')[1:]        # Path elements 0 = printer 1 = file
      #self.files[pe[1]] += buf
      #return len(buf)
      return 0

  def release(self, path, flags):
      #pe = path.split('/')[1:]        # Path elements 0 = printer 1 = file
      #if len(self.files[pe[1]]) > 0:
          #lpr = Popen(['lpr -P ' + pe[0]], shell=True, stdin=PIPE)
          #lpr.communicate(input=self.files[pe[1]])
          #lpr.wait()
          #self.lastfiles[pe[1]] = self.files[pe[1]]
          #self.files[pe[1]] = ""      # Clear out string
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



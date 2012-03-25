#!/usr/bin/env python2
import webkit
import gtk
import os
import fusefb
import fbjson

facebook_auth_uri = "https://www.facebook.com/dialog/oauth?client_id=336398709742529&redirect_uri= https://www.facebook.com/connect/login_success.html&response_type=token"


def get_token():
    folder = os.getenv('HOME') + "/.fbfs/token"
    if os.path.exists(folder):
        token_file = open(folder, 'r')
        return token_file.read()
    else:
        browser = Browser()
        gtk.main()

class Browser(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        vbox = gtk.VBox(spacing=1)
        webpage = webkit.WebView()
        scroller = gtk.ScrolledWindow()
        scroller.add(webpage)
        vbox.pack_start(scroller)
        self.add(vbox)
        self.set_title("Authorization")
        self.resize(400, 400)
        webpage.load_uri(facebook_auth_uri)
        self.show_all()



if __name__ == "__main__":
    token = get_token()
    fbjson.token = token
    server = fusefb.FacebookFS()
    server.parse(errex=1)
    server.main()

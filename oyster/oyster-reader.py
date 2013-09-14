#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sudo apt-get install python-gtk2 python-pip flite
# sudo pip install wikipedia

import pygtk
pygtk.require('2.0')

import gtk
import ConfigParser
from datetime import datetime
import subprocess
import time

import wikipedia

#flite -voice rms "Hello Chuck - ticket valid"


class Application():
    
    def __init__(self):
        # Config
        self.config = ConfigParser.ConfigParser()
        self.config.read("cards.ini")
        self.open =  datetime.strptime(self.config.get("General", "open"), "%H:%M").time()
        self.close =  datetime.strptime(self.config.get("General", "close"), "%H:%M").time()
        self.goodnightcount = 0
        self.goodnight = self.config.get("General", "goodnight")
        self.reallygoodnight = self.config.get("General", "reallygoodnight")
        self.salute =  self.config.get("General", "salute")
#        print self.open, self.close, self.salute
        self.cards = []
        for section in self.config.sections():
            if section == "General":
                pass
            elif section == "Notlisted":
                pass
            else:
                self.cards.append(section)
        # gtk
        self.window = gtk.Window()
        self.window.set_title("Charlie's Classroom Shop Bed - Oyster Reader")
        
        self.create_widgets()
        self.connect_signals()
        
        self.window.show_all()
#        self.window.fullscreen()
        gtk.main()
    
    
    def create_widgets(self):

        #vbox = gtk.VBox()
        self.image = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file("logo/logo.png")
        #get_height()
        scaled_buf = pixbuf.scale_simple(320,320,gtk.gdk.INTERP_BILINEAR)
        self.image.set_from_pixbuf(scaled_buf)
        self.text = gtk.Label()
        self.text.set_markup('<span size="x-large" weight="bold">Welcome to \nCharlie\'s Classroom Shop Bed</span>')
        self.text.set_width_chars(40)
        self.text.set_line_wrap(True)
        self.hbox_1 = gtk.HBox(spacing=10)
        self.hbox_1.pack_start(self.image)
        self.hbox_1.pack_start(self.text, expand=False)

        self.label = gtk.Label("Please scan your oyster")
        self.entry = gtk.Entry()
        self.entry.set_invisible_char("*")
        self.entry.set_visibility(False)
        self.button_exit = gtk.Button("Exit")

        self.hbox_2 = gtk.HBox(spacing=10)
        self.hbox_2.pack_start(self.label)
        self.hbox_2.pack_start(self.entry)
        self.hbox_2.pack_start(self.button_exit)

        self.vbox = gtk.VBox(spacing=10)
        self.vbox.pack_start(self.hbox_1)
        self.vbox.pack_start(self.hbox_2, expand=False)
        
        self.window.add(self.vbox)
    
    def connect_signals(self):
        self.button_exit.connect("clicked", self.callback_exit)
        self.entry.connect("activate", self.callback_scan)    

    def flite(self, text):
        for t in text.split("\n"):
            if t <> "":
                s = subprocess.call(["flite", "--setf", "duration_stretch=1.25", "-voice", "rms", t])
            time.sleep(0.5)

    def callback_scan(self, widget, callback_data=None):
        scan = self.entry.get_text()
        self.entry.set_text("")
        print "Scanned: ", scan
        if self.open <= datetime.now().time() <= self.close:
            if scan not in self.cards:
                scan = "Notlisted"
            actions =  self.config.get(scan, "actions")
            text = self.config.get(scan, "name") + " \n" + self.config.get(scan, "extra")
            if "access" in actions:
                try:
                    pixbuf = gtk.gdk.pixbuf_new_from_file(self.config.get(scan, "photo"))
                    #get_height()
                    scaled_buf = pixbuf.scale_simple(320,320,gtk.gdk.INTERP_BILINEAR)
                    self.image.set_from_pixbuf(scaled_buf)
                except:
                    pass
                text = self.salute + " " + text
            if "wikipedia" in actions:
               text = text + '\n' + wikipedia.summary(wikipedia.random(pages=1), sentences=3)
    
            # Make carriage return for each sentence. To allow pause between each sentenance.
            text = text.replace('?', '\n')
            text = text.replace('.', '\n')
            self.text.set_markup('<span size="x-large" weight="bold">' + text + '</span>')
            while gtk.events_pending():
               gtk.main_iteration(False)
            time.sleep(1)
            self.flite(text)
            self.goodnightcount = 0
        else:        
            text = " " + datetime.now().time().strftime("%H:%M") + '\n'
            if self.goodnightcount == 1:
                text = text + self.reallygoodnight
                self.flite(text)
                self.goodnightcount = 2
            if self.goodnightcount == 0:
                text = text + self.goodnight
                self.flite(text)
                self.goodnightcount = 1

    
    def callback_exit(self, widget, callback_data=None):
        gtk.main_quit()
    

if __name__ == "__main__":
    app = Application()


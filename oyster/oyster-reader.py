#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')

import gtk

#flite -voice rms "Hello Chuck - ticket valid"


class Application():
    
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title("Charlie's Classroom Shop Bed - Oyster Reader")
        
        self.create_widgets()
        self.connect_signals()
        
        self.window.show_all()
        self.window.fullscreen()
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
        self.hbox_1 = gtk.HBox(spacing=10)
        self.hbox_1.pack_start(self.image)
        self.hbox_1.pack_start(self.text)

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
        self.entry.connect("activate", self.callback_ok)
    
    def callback_ok(self, widget, callback_data=None):
        name = self.entry.get_text()
        self.entry.set_text("")

        print name
    
    
    def callback_exit(self, widget, callback_data=None):
        gtk.main_quit()
    

if __name__ == "__main__":
    app = Application()


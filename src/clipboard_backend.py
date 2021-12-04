# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(asctime)s %(pathname)s, %(funcName)s:%(lineno)d: %(message)s")

import threading
import time
import chardet
import traceback
from subprocess import Popen, PIPE

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

class ClipboardBackend:

    stop_thread = False
    callback = None
    current_cb_data = None

    def __init__(self, callback=None):
        logging.info("clipboard backend started")

        self.callback = callback

        def init_manager():
            while True: 
                if self.stop_thread:
                    break
                self.check_clipboard()
                time.sleep(5)

        self.thread = threading.Thread(target=init_manager)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.stop_thread = True
        logging.info("clipboard backend stopped")

    def check_clipboard(self):
        ''' Checks if clipboard has any data or has changed '''
        try:
            get_types = Popen(['wl-paste', '--list-types'], stdout=PIPE)
            stdout, stderr = get_types.communicate()
            cb_types = stdout

            get_data = Popen(['wl-paste'], stdout=PIPE)
            stdout, stderr = get_data.communicate()
            cb_data = stdout
            
            logging.info(cb_types)
            
            # if self.current_cb_data != cb_data:
                # logging.info("\nclipboard data:\n{0}".format(cb_data.decode(chardet.detect(stdout)["encoding"])))
                # self.current_cb_data = cb_data
                # GLib.idle_add(self.callback, cb_data.decode(chardet.detect(stdout)["encoding"]))
        except:
            logging.error(traceback.format_exc())


class ClipsWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.label = Gtk.Label()
        self.set_child(self.label)
        self.set_size_request(480, 360)
        self.present()

    def set_label(self, text):
        self.label.props.label = text


class Application(Gtk.Application):

    app_id = "com.github.hezral.clips"
    window = None

    def __init__(self):
        super().__init__()

        self.props.application_id = self.app_id

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        if self.window is None:
            self.window = ClipsWindow(application=self)
            self.add_window(self.window)

        cb = ClipboardBackend(callback=self.window.set_label)

app = Application()
app.run(None)

# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

# SPDX-License-Identifier: MIT License
# SPDX-FileCopyrightText: 2018 emersion <contact@emersion.fr>
# Original https://github.com/emersion/hello-wayland/tree/selection

import traceback
import logging
# logging.basicConfig(level=logging.debug, format="%(levelname)s: %(asctime)s %(pathname)s, %(funcName)s:%(lineno)d: %(message)s")
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(funcName)s:%(lineno)d: %(message)s")

import os
import io

import pywayland
from pywayland import client, server
from pywayland.protocol.wayland import *

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

class WlDataSourceListener(WlDataSource):
    def __init__(self, send_callback, cancelled_callback, *args, **kwargs):
        super().__init__()
        self.send_callback = send_callback
        self.cancelled_callback = cancelled_callback

    def send(self):
        return self.send_callback
    
    def cancelled(self):
        return self.cancelled_callback


class WlDataOfferListener(WlDataOffer):
    def __init__(self, offer_callback, *args, **kwargs):
        super().__init__()
        self.offer_callback = offer_callback

    def offer(self):
        return self.offer_callback


class WlDataDeviceListener(WlDataDevice):
    def __init__(self, data_offer_callback, selection_callback, *args, **kwargs):
        super().__init__()
        self.data_offer_callback = data_offer_callback
        self.selection_callback = selection_callback

    def data_offer(self):
        return self.offer_callback

    def selection(self):
        return self.selection_callback


class WlKeyboardListener(WlKeyboard):
    def __init__(self, keymap_callback, enter_callback, leave_callback, key_callback, modifiers_callback, repeat_info_callback, *args, **kwargs):
        super().__init__()
        self.keymap_callback = keymap_callback
        self.enter_callback = enter_callback
        self.leave_callback = leave_callback
        self.key_callback = key_callback
        self.modifiers_callback = modifiers_callback
        self.repeat_info = repeat_info_callback

    def keymap(self):
        return self.key_callback
    
    def enter(self):
        return self.enter_callback

    def leave(self):
        ...
    
    def key(self):
        return self.key_callback

    def modifiers(self):
        ...

    def repeeat_info(self):
        ...


class WlSeatListener(WlSeat):
    def __init__(self, capabilities_callback, *args, **kwargs):
        super().__init__()
        self.capabilities_callback = capabilities_callback
    
    def capabilities(self):
        return self.capabilities_callback



class PywaylandBackend():

    running = True
    shm_data = None
    keyboard_enter_serial = 0
    text = "Hello Wayland Clipboard!"
    html = "<strong>Hello Wayland Clipboard!</strong>"

    # data_device_manager = WlDataDeviceManager()
    # logging.debug(data_device_manager)

    # surface = WlSurface()
    # logging.debug(surface)

    # data_device = WlDataDevice()
    # logging.debug(data_device)



    def __init__(self, *args, **kwargs):
        super().__init__()

        self.display = client.Display()
        try:
            self.display.connect()
            logging.debug("Connected:{0}".format(self.display))
        except:
            logging.error(traceback.format_exc())

        self.registry = self.display.get_registry()
        logging.debug(self.registry)
        self.registry.dispatcher["global"] = self.handle_global
        self.registry.dispatcher["global_remove"] = self.handle_global

        self.display.dispatch(block=True)
        self.display.roundtrip()

        if self.seat:
            self.data_device = self.data_device_manager.get_data_device(self.seat)
            logging.debug(self.data_device)
            self.data_device.dispatcher["data_offer"] = self.data_device_handle_data_offer
            self.data_device.dispatcher["selection"] = self.data_device_handle_selection

        # self.data_source_listener = WlDataSourceListener(
        #     send_callback=self.data_source_handle_send,
        #     cancelled_callback=self.data_source_handle_cancelled
        # )
        # logging.debug(self.data_source_listener)
        # logging.debug(self.data_source_listener.name)

        # self.data_offer_listener = WlDataOfferListener(
        #     offer_callback=self.data_offer_handle_offer
        # )
        # logging.debug(self.data_offer_listener)

        # self.data_device_listener = WlDataDeviceListener(
        #     data_offer_callback=self.data_device_handle_data_offer,
        #     selection_callback=self.data_device_handle_selection
        # )
        # logging.debug(self.data_device_listener)
        # logging.debug(self.data_device_listener)

        # self.keyboard_listener = WlKeyboardListener(
        #     keymap_callback=self.keyboard_handle_keymap,
        #     enter_callback=self.keyboard_handle_enter,
        #     leave_callback=None,
        #     key_callback = self.keyboard_handle_key,
        #     modifiers_callback=None,
        #     repeat_info_callback=None
        # )
        # logging.debug(self.keyboard_listener)

        # self.seat_listener = WlSeatListener(
        #     capabilities_callback=self.seat_handle_capabilities
        # )
        # logging.debug(self.seat_listener)

    def shm_format_handler(self, shm, format_):
        if format_ == WlShm.format.argb8888.value:
            s = "ARGB8888"
        elif format_ == WlShm.format.xrgb8888.value:
            s = "XRGB8888"
        elif format_ == WlShm.format.rgb565.value:
            s = "RGB565"
        else:
            s = "other format"
        # logging.debug("Possible shmem format: {0},{1}".format(s, format_))
        ...

    def data_source_handle_send(self, data, source, mime_type, fd):
        '''an application wants to paste the clipboard contents'''
        if "text/plain" in mime_type:
            os.write(fd, str.encode(self.text))
        elif "text/html" in mime_type:
            os.write(fd, str.encode(self.html))
        else:
            logging.error("Destination client requested unsupported MIME type:{0}".format(mime_type))
        os.close(fd)

    def data_source_handle_cancelled(self, data, source):
        '''an application has replaced the clipboard contents'''
        source.destroy()

    def data_offer_handle_offer(self, data, offer, mime_type):
        logging.debug("Clipboard supports MIME types:\n{0}".format(mime_type))

    # def data_device_handle_data_offer(self, data, data_device, offer):
    def data_device_handle_data_offer(self, *args):
        logging.debug(locals())
        # wl_data_offer_add_listener(offer, &data_offer_listener, NULL);
        ...

    def data_device_handle_selection(self, data, data_device, offer):
        '''an application has set the clipboard contents'''
        if offer is None:
            logging.error("Clipboard is empty")
            return
        
        fds = [0] * 2
        fds[0], fds[1] = os.pipe()

        self.data_offer_listener.receive("text/plain", fds[1])
        os.close(fds[1])

        self.display.roundtrip()

        # read the clipboard contents and print it to the standard output
        logging.debug("Clipboard data:\n")
        while True:
            buf = bytearray(1024)
            with io.open(fds[0], 'rb') as fp:
                size = fp.readinto(buf)
                if not size:
                    break
                # do things with buf considering the size
                fp.write(size)

        os.close(fds[0])
        offer.destroy()
        
    def keyboard_handle_keymap(self, data, keyboard, format, fd, size):
        os.close(fd)

    def keyboard_handle_enter(self, data, keyboard, serial, surface, keys):
        self.keyboard_enter_serial = serial

    def keyboard_handle_key(self, data, keyboard, serial, time, key, state):
        # if (state != WL_KEYBOARD_KEY_STATE_RELEASED) {
        #     return;
        # }
        logging.debug(state)
        
        self.data_source = self.data_device_manager.create_data_source()
        # setup a listener to receive wl_data_source_events
        self.data_source.dispatcher["send"] = self.data_source_handle_send
        self.data_source.dispatcher["cancelled"] = self.data_source_handle_cancelled()

        # advertise MIME types
        self.data_source.offer(self.data_sourc, "text/plain")
        self.data_source.offer(self.data_sourc, "text/html")
        self.data_device.set_selection(self.data_source, self.keyboard_enter_serial)
        
    def seat_handle_capabilities(self, data, seat, capabilities):
        # if (capabilities & WL_SEAT_CAPABILITY_KEYBOARD) {
        #     struct wl_keyboard *keyboard = wl_seat_get_keyboard(seat);
        #     wl_keyboard_add_listener(keyboard, &keyboard_listener, seat);
        # }
        logging.debug(capabilities)

    def handle_global(self, registry, id_, interface, version):
        if interface == "wl_shm":
            self.shm = registry.bind(id_, WlShm, version)
            self.shm.dispatcher["format"] = self.shm_format_handler
            logging.debug(self.shm)
        elif interface == "wl_seat":
            self.seat = registry.bind(id_, WlSeat, version)
            # wl_seat_add_listener(seat, &seat_listener, NULL);
        elif interface == "wl_compositor":
            self.compositor = registry.bind(id_, WlCompositor, version)
            logging.debug(self.compositor)
        elif interface == "wl_data_device_manager":
            self.data_device_manager = registry.bind(id_, WlDataDeviceManager, version)
            logging.debug(self.data_device_manager)

    def handle_global_remove(self, registry, id_):
        logging.debug(locals())


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

pywayland_backend = PywaylandBackend()
app = Application()
app.run(None)
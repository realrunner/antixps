__author__ = 'mnelson'

from threading import Lock
import logging
import os
import urllib.request, urllib.parse, urllib.error
import io

from escpos import printer
import qrcode
import usb.core
import usb.util

PRINTER_CLASS = 7

logger = logging.getLogger("Printing")

printers = {}


def get_printer(serial, cfg):
    cfg_printer = None
    for p in cfg.printers:
        if p["serial"] == serial:
            cfg_printer = p
            break

    if cfg_printer is None:
        return None

    if serial in printers:
        return printers[serial]
    else:
        p = Printer(cfg_printer, cfg)
        printers[serial] = p
        return p


class CustomPrinter(printer.Usb):
    def __init__(self, idVendor, idProduct, bus, address):
        self.bus = bus
        self.address = address
        printer.Usb.__init__(self, idVendor, idProduct)

    def qr(self, text):
        """ Print QR Code for the provided string """
        qr_code = qrcode.QRCode(version=4, box_size=6, border=1)
        qr_code.add_data(text)
        qr_code.make(fit=True)
        qr_img = qr_code.make_image()
        im = qr_img._img.convert("RGB")
        # Convert the RGB image in printable image
        self._convert_image(im)

    def open(self):
        """ Search device on USB tree and set is as escpos device """
        self.device = usb.core.find(idVendor=self.idVendor, idProduct=self.idProduct, address=self.address,
                                    bus=self.bus)
        if self.device is None:
            print("Cable isn't plugged in")
            return

        # self.device.set_configuration()
        try:
            if self.device.is_kernel_driver_active(0):
                try:
                    self.device.detach_kernel_driver(0)
                except usb.core.USBError as e:
                    print("Could not detatch kernel driver: %s" % str(e))
        except NotImplementedError as e2:
            pass
        except Exception as e3:
            print("Could not check if kernel driver is active %s " % str(e3))

        try:
            self.device.set_configuration()
            self.device.reset()
        except usb.core.USBError as e:
            print("Could not set configuration: %s" % str(e))

    def reset(self):
        pass
        # self.hw('RESET')


class Command(object):
    """ Commands Supported
        {"command": "text", "text": "Some very interesting text"}
        {"command": "cut"}
        {"command": "cashdraw", "pin": 2}
        {"command": "reset"}
        {"command": "qr", "data": "Some nice textual data"}
        {"command": "image", "path": "path_or_url_to_image"}
        {"command": "set", "align": "left|center|right", "font": "b|a", "type": "normal|b|u|u2|bu|bu2", "width":1|2, "height": 1|2}
    """

    def __init__(self, details, cfg):
        self.cfg = cfg
        self.details = details
        if 'text' in self.details and not self.details['text'].endswith("\n"):
            self.details['text'] += "\n"

    def send(self, _printer):
        {
            "text": lambda: _printer.text(self.details['text']),
            "cut": lambda: _printer.cut(),
            "cashdraw": lambda: _printer.cashdraw(self.details['pin']),
            "reset": lambda: _printer.reset(),
            "qr": lambda: _printer.qr(self.details['data']),
            "image": lambda: _printer.image(self.fetch_image(self.details['path'])),
            "set": lambda: _printer.set(**dict([(k, v) for k, v in self.details.items() if k != 'command'])),
        }[self.details['command']]()

    def fetch_image(self, path):
        if os.path.exists(path):
            return path
        if path.startswith('/'):
            path = self.cfg.app_url + path
        image_data = urllib.request.urlopen(path).read()
        fp = io.StringIO(image_data)
        return fp

    def __str__(self):
        return str(self.details)


class Printer(object):
    def __init__(self, cfg_printer, cfg):
        self.config = cfg_printer
        self.cfg = cfg
        self.lock = Lock()
        self.reset()

    def print_receipt(self, commands):
        try:
            self.lock.acquire()
            p = self.get_printer()
            self._print(p, commands)
            del p
        except Exception as ex:
            import traceback

            traceback.print_exc()
            logger.error("Failed initializing configured printer: " + str(ex))
        finally:
            self.lock.release()

    def reset(self):
        try:
            self.lock.acquire()
            p = self.get_printer()
            del p
        except Exception as ex:
            import traceback

            traceback.print_exc()
            logger.error("Failed initializing configured printer: " + str(ex))
        finally:
            self.lock.release()

    def get_printer(self):
        vendor = self.config["idVendor"]
        product = self.config["idProduct"]
        address = self.config["address"]
        bus = self.config["bus"]
        p = CustomPrinter(vendor, product, bus, address)
        p.reset()
        return p

    def _print(self, _printer, commands):
        for details in commands:
            command = Command(details, self.cfg)
            try:
                command.send(_printer)
            except Exception as ex:
                logger.warn("Failed print command: {0}\n{1}".format(command, ex))
                pass


def find_printers():
    return [{"idProduct": d.idProduct,
             "idVendor": d.idVendor,
             "address": d.address,
             "bus": d.bus,
             "manufacturer": usb.util.get_string(d, 1),
             "model": usb.util.get_string(d, 2),
             "serial": usb.util.get_string(d, 3)}
            for d in usb.core.find(find_all=1, custom_match=FindClass(PRINTER_CLASS))]


def merge_connected_with_config(connected, config):
    conn_map = dict([(d['serial'], d) for d in connected])
    config_map = dict([(d['serial'], d) for d in config.printers])
    for d in connected:
        if d['serial'] in config_map:
            config_map[d['serial']].update(d)
        else:
            config_map[d['serial']] = d
            config_map[d['serial']]["name"] = d['serial']
            config.printers.append(config_map[d['serial']])
        config_map[d['serial']]["connected"] = True
    for d in config.printers:
        if d['serial'] not in conn_map:
            d["connected"] = False


class FindClass(object):
    def __init__(self, class_):
        self._class = class_

    def __call__(self, device):
        # first, let's check the device
        if device.bDeviceClass == self._class:
            return True
        # ok, transverse all devices to find an
        # interface that matches our class
        for cfg in device:
            # find_descriptor: what's it?
            intf = usb.util.find_descriptor(
                cfg,
                bInterfaceClass=self._class
            )
            if intf is not None:
                return True

        return False


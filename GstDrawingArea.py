import GstCV
import gi

gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gst, Gtk, GObject, GLib
import cairo
from PIL import Image
import numpy
import threading


class GstDrawingArea(Gtk.DrawingArea):
    # __gsignals__ = {"expose-event": "override", "unrealize": "override"}

    def __init__(self, IP="127.0.0.1", RTP_RECV_PORT0=5000, RTCP_RECV_PORT0=5001, RTCP_SEND_PORT0=5005, codec="JPEG",
                 resolution=[640, 480]):
        Gtk.DrawingArea.__init__(self)
        # super(GstDrawingArea, self).__init__(self)  # инициализируем DrawingArea
        self.resolution = resolution
        """видео:"""
        self.source = GstCV.CVGstreamer(IP, RTP_RECV_PORT0, RTCP_RECV_PORT0, RTCP_SEND_PORT0, codec="JPEG")
        self.connect("draw", self.doDraw)
        self.connect("unrealize", self.doUnrealize)
        self.set_size_request(resolution[0], resolution[1])
        self.img = None
        GLib.timeout_add(7, self.on_timer)

    def doDraw(self, widget, cr):
        if self.source.cvImage is not None:
            # print(self.source.cvImage)
            height, width, channels = self.source.cvImage.shape
            # print(self.source.cvImage.flat)
            self.img = Image.frombytes("RGB", [width, height], self.source.cvImage.flatten(), "raw", "RGB")
            self.img.putalpha(255)
            arr = numpy.array(self.img)
            surface = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_RGB24, width, height)
            pt1 = cairo.SurfacePattern(surface)
            pt1.set_extend(cairo.EXTEND_REPEAT)
            cr.set_source(pt1)
            cr.rectangle(0, 0, self.resolution[0], self.resolution[1])
            cr.fill()
            return False

    def on_timer(self):     # если возвращает True будет рендериться вечно, False - не рендерится
        self.queue_draw()
        return True     #

    def doUnrealize(self, arg):
        self.source.stop()

    def start(self):
        self.source.start()

    def stop(self):
        self.source.stop()

    def paused(self):
        self.source.paused()

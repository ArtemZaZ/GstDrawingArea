import gi

gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
import GstDrawingArea
from gi.repository import Gtk, GLib, GObject

IP = '127.0.0.1'
RTP_RECV_PORT0 = 5000
RTCP_RECV_PORT0 = 5001
RTCP_SEND_PORT0 = 5005


def defaultDraw(self, widget, cr):
    pass


class Pult:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("test.glade")
        self.window = self.builder.get_object("window1")
        self.button = self.builder.get_object("button1")
        self.box = self.builder.get_object("box2")  # бокс под виджет видео-gstreamera
        self.window.connect("delete-event", self.delete_event)

        self.GDA = GstDrawingArea.GstDrawingArea(resolution=[640, 480], drawCallBack=defaultDraw)  # виджет gstreamera
        self.box.pack_start(self.GDA, True, True, 0)
        self.GDA.setSource(IP, RTP_RECV_PORT0, RTCP_RECV_PORT0, RTCP_SEND_PORT0, codec='JPEG')
        self.window.show_all()

        self.GDA.source.start()

        Gtk.main()

    def delete_event(self, widget, event, data=None):
        self.GDA.source.stop()
        Gtk.main_quit()


p = Pult()
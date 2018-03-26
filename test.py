import gi

gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
import GstDrawingArea
from gi.repository import Gtk, GLib, GObject


class Pult:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("test.glade")
        self.window = self.builder.get_object("window1")
        self.button = self.builder.get_object("button1")
        self.box = self.builder.get_object("box2")  # бокс под виджет видео-gstreamera
        self.window.connect("delete-event", self.delete_event)

        self.GDA = GstDrawingArea.GstDrawingArea()  # виджет gstreamera
        self.box.pack_start(self.GDA, True, True, 0)

        self.window.show_all()

        self.GDA.source.start()

        Gtk.main()

    def delete_event(self, widget, event, data=None):
        self.GDA.stop()
        Gtk.main_quit()


p = Pult()
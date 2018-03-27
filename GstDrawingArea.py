import GstCV
import gi
import cairo
import numpy
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gst, Gtk, GObject, GLib


def defaultDraw(self, widget, cr):
    pass


class GstDrawingArea(Gtk.DrawingArea):
    # __gsignals__ = {"expose-event": "override", "unrealize": "override"}

    def __init__(self, IP="127.0.0.1", RTP_RECV_PORT0=5000, RTCP_RECV_PORT0=5001, RTCP_SEND_PORT0=5005, codec="JPEG",
                 resolution=[640, 480], drawCallBack=defaultDraw):
        Gtk.DrawingArea.__init__(self)  # инициализируем родителя
        self.resolution = resolution    # разрешение
        """видео:"""
        self.source = GstCV.CVGstreamer(IP, RTP_RECV_PORT0, RTCP_RECV_PORT0, RTCP_SEND_PORT0, codec=codec)
        self.connect("draw", self.doDraw)   # привязка отрисовки
        self.connect("unrealize", self.doUnrealize)     # привязка освобождения ресурсов
        self.set_size_request(resolution[0], resolution[1])     # ставим разрешение на виджет
        self.img = None     # изображение с альфа-каналом
        self.drawCallBack = drawCallBack    # устанавливаем ф-ию внешней отрисовки
        GLib.timeout_add(10, self.on_timer)

    def doDraw(self, widget, cr):       # ф-ия вызывается при отрисовке
        if self.source.cvImage is not None:
            height, width, channels = self.source.cvImage.shape
            z = numpy.full((height, width, 1), 255, dtype=numpy.uint8)  # создаем массив 3х3 и заполняем глубину
            # значением 255
            self.img = numpy.append(self.source.cvImage, z, axis=2)     # Добавляем к каждому пикселю значение
            # альфа-канала
            surface = cairo.ImageSurface.create_for_data(self.img, cairo.FORMAT_RGB24, width, height)
            pt1 = cairo.SurfacePattern(surface)
            pt1.set_extend(cairo.EXTEND_REPEAT)
            cr.set_source(pt1)
            cr.rectangle(0, 0, self.resolution[0], self.resolution[1])
            cr.fill()
            self.drawCallBack(self, width, cr)
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

    def drawCallBack(self, widget, cr):     # перегружаемая ф-ия для отрисовки
        pass

import GstCV
import gi
import cairo
import numpy
import math
from PIL import Image
gi.require_version("Gst", "1.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gst, Gtk, GObject, GLib


def defaultDraw(self, widget, cr):
    pass


class WaitIndicator(object):
    trs = (
        (0.0, 0.15, 0.30, 0.5, 0.65, 0.80, 0.9, 1.0),
        (1.0, 0.0, 0.15, 0.30, 0.5, 0.65, 0.8, 0.9),
        (0.9, 1.0, 0.0, 0.15, 0.3, 0.5, 0.65, 0.8),
        (0.8, 0.9, 1.0, 0.0, 0.15, 0.3, 0.5, 0.65),
        (0.65, 0.8, 0.9, 1.0, 0.0, 0.15, 0.3, 0.5),
        (0.5, 0.65, 0.8, 0.9, 1.0, 0.0, 0.15, 0.3),
        (0.3, 0.5, 0.65, 0.8, 0.9, 1.0, 0.0, 0.15),
        (0.15, 0.3, 0.5, 0.65, 0.8, 0.9, 1.0, 0.0)
    )

    CLIMIT = 1000
    NLINES = 8


class GstDrawingArea(Gtk.DrawingArea):
    # __gsignals__ = {"expose-event": "override", "unrealize": "override"}

    def __init__(self, IP="127.0.0.1", RTP_RECV_PORT0=5000, RTCP_RECV_PORT0=5001, RTCP_SEND_PORT0=5005, codec="JPEG",
                 resolution=[640, 480], drawCallBack=defaultDraw):
        Gtk.DrawingArea.__init__(self)  # инициализируем родителя
        self.resolution = resolution    # начальное разрешение
        """видео:"""
        self.source = None # GstCV.CVGstreamer(IP, RTP_RECV_PORT0, RTCP_RECV_PORT0, RTCP_SEND_PORT0, codec=codec)
        self.connect("draw", self.doDraw)   # привязка отрисовки
        self.connect("unrealize", self.doUnrealize)     # привязка освобождения ресурсов
        self.set_size_request(resolution[0], resolution[1])     # ставим разрешение на виджет
        self.img = None     # изображение с альфа-каналом
        self.drawCallBack = drawCallBack    # устанавливаем ф-ию внешней отрисовки
        GLib.timeout_add(10, self.on_timer)     # дергаем раз  в 10 мс ф-ию on_timer
        self.waitIndicatorCount = 0

    def doDraw(self, widget, cr):       # ф-ия вызывается при отрисовке
        if self.source is not None:     # если ресурс камеры создан
            if self.source.cvImage is not None:     # если изображение существует
                height, width, channels = self.source.cvImage.shape     # получаем данные из кадра камеры
                limg = Image.frombytes("RGB", [width, height], self.source.cvImage.flatten(), "raw")    # создаем
                #  изображение PIL
                widgetAlloc = self.get_allocation()   # получаем координаты и размеры виджета
                self.img = limg.resize((widgetAlloc.width, widgetAlloc.height), Image.ANTIALIAS)    # изменяем
                # размер изображение до размера виджета
                self.img.putalpha(255)  # создаем альфа-канал
                arr = numpy.array(self.img)     # создаем массив из изображения
                surface = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_RGB24, widgetAlloc.width, widgetAlloc.height)
                pt1 = cairo.SurfacePattern(surface)
                pt1.set_extend(cairo.EXTEND_REPEAT)
                cr.set_source(pt1)
                cr.rectangle(0, 0, widgetAlloc.width, widgetAlloc.height)
                cr.fill()
                self.drawCallBack(self, widget, cr)
            else:
                self.drawWaitIndicator(cr)
            return False
        else:
            pass

    def on_timer(self):     # если возвращает True будет рендериться вечно, False - не рендерится
        self.queue_draw()
        self.waitIndicatorCount = self.waitIndicatorCount + 0.1
        if self.waitIndicatorCount >= WaitIndicator.CLIMIT:
            self.waitIndicatorCount = 0
        return True     #

    def setSource(self, IP="127.0.0.1", RTP_RECV_PORT0=5000, RTCP_RECV_PORT0=5001, RTCP_SEND_PORT0=5005, codec="JPEG"):
        self.source = GstCV.CVGstreamer(IP, RTP_RECV_PORT0, RTCP_RECV_PORT0, RTCP_SEND_PORT0, codec=codec)

    def doUnrealize(self, arg):
        if self.source is not None:
            self.source.stop()
            self.source = None

    def drawCallBack(self, widget, cr):     # перегружаемая ф-ия для отрисовки
        pass

    def drawWaitIndicator(self, cr):
        cr.set_line_width(3)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        widgetAlloc = self.get_allocation()   # получаем координаты и размеры виджета

        cr.translate(widgetAlloc.width / 2, widgetAlloc.height / 2)

        for i in range(WaitIndicator.NLINES):
            cr.set_source_rgba(0, 0, 0, WaitIndicator.trs[int(self.waitIndicatorCount) % 8][i])
            cr.move_to(0.0, -10.0)
            cr.line_to(0.0, -40.0)
            cr.rotate(math.pi / 4)
            cr.stroke()


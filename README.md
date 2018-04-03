# GstDrawingArea
Виджет Gtk для вывода видео(rtcp протокол) в окно Gtk + возможности Gtk DrawingArea
## Import
Чтобы импортировать данный модуль необходимо в файле программы ввести
```
import GstDrawingArea
```
## Связь
Т.к. видео передается через rtcp, необходимо указать ip(передающего устройства) и порты для связи
```
IP = '127.0.0.1'
RTP_RECV_PORT0 = 5000
RTCP_RECV_PORT0 = 5001
RTCP_SEND_PORT0 = 5005
```
## GstDrawingArea
Класс, который наследуется от виджета GTK - DrawingArea, соответственно все методы доступные DrawingArea доступны и этому классу
Параметрами конструктора являются начальное разрешение виджета - **resolution**, внешняя ф-ия отрисовки - **drawCallBack**, которая имеет формат
**defaultDraw**

```
def defaultDraw(self, widget, cr):
    pass
    

GDA = GstDrawingArea.GstDrawingArea(resolution=[640, 480], drawCallBack=defaultDraw)
```
## Упаковка
Упаковка виджета в графическое приложение производится также, как и упаковка обычного виджета                          
```
box.pack_start(GDA, True, True, 0)
```
## Методы
Установить ресурс камеры. В качастве параметров передаются ip, порты, какой нужен кодек('JPEG' или 'H264').
```
GDA.setSource(IP, RTP_RECV_PORT0, RTCP_RECV_PORT0, RTCP_SEND_PORT0, codec='JPEG')
```
Запуск видео
```
GDA.source.start()
```
Пауза
```
GDA.source.paused()
```
Остановка видео с освобождением ресурсов
```
GDA.source.stop()
```

Пример работы с модулем в файле test.py

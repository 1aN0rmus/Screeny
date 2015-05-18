import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import urllib2

tgturl = sys.argv[1]
print tgturl

class Screenshot(QWebView):
    def __init__(self):
        self.app = QApplication(sys.argv)
        QWebView.__init__(self)
        self._loaded = False
        self.loadFinished.connect(self._loadFinished)

    def capture(self, url, output_file):
        self.load(QUrl(url))
        self.wait_load()
        # set to webpage size
        frame = self.page().mainFrame()
        self.page().setViewportSize(frame.contentsSize())
        # render image
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        print 'saving', output_file
        image.save(output_file)

    def wait_load(self, delay=0):
        # process app events until page loaded
        while not self._loaded:
            self.app.processEvents()
            time.sleep(delay)
        self._loaded = False

    def _loadFinished(self, result):
        self._loaded = True

req = urllib2.Request(tgturl)
try:
    resp = urllib2.urlopen(req)
except urllib2.HTTPError as e:
    if e.code == 404:
        print tgturl + ' ' + str(e.code)
	pass
except urllib2.URLError as e:
	print 'you got an error with the code', e
else:
    # 200
    body = resp.read()
    s = Screenshot()
    s.capture(tgturl, './img/' + tgturl[7:] + '.png')

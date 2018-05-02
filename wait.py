import wx
import threading
from time import sleep


class Wait(threading.Thread):
    def __init__(self, option_id):
        threading.Thread.__init__(self)
        self.option_id = option_id

    def run(self):
        sleep(1)

#        self.object.SetForegroundColour(wx.Colour(255, 0, 0))
#        self.object.Show()
        print('inwait')

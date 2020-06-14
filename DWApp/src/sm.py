from kivy.uix.screenmanager import ScreenManager
from girissayfasi import GirisSayfasi
from distropage import DistroPage


class SM(ScreenManager):

    def __init__(self):

        super().__init__()
        self.add_widget(GirisSayfasi())
        self.current = 'girisSayfasi'

    def openDistroPage(self,distro):
        
        dp = DistroPage(distro)
        if dp.exist:
            if distro not in self.screen_names:
                self.add_widget(dp)
            self.current = distro
        else:
            pass
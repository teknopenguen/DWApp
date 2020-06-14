from kivy.uix.screenmanager import Screen
from kivy.uix.image import AsyncImage
from kivymd.uix.list import ThreeLineListItem
from kivy.base import runTouchApp
from kivy.lang import Builder
from dwparser import DWParser
from settings import TEMPLATE_DIR
from os import path

kv_file = path.join(path.join(TEMPLATE_DIR, 'distropage.kv'))
Builder.load_file(kv_file)


class PaginationImage(Screen):
    pass


class DistroPage(Screen):

    dwparser = DWParser('https://www.distrowatch.com/')

    def __init__(self, distro):
        super().__init__()
        self.ids.logo_paginator.manager = self.ids.logo
        self.ids.logo.paginator = self.ids.logo_paginator
        self.name = distro
        self.exist = True
        self.distro = distro
        self.createContent()
        
    def createPaginationImage(self, array):

        self.ids.logo.clear_widgets()
        self.ids.logo_paginator.items_round_paginator = []
        array = list(array)
        for i in reversed(array):
            pi = PaginationImage()
            image = AsyncImage(source=i)
            pi.name = 'image' + str(array.index(i)+1)
            pi.add_widget(image)
            self.ids.logo.add_widget(pi)
        
        self.ids.logo_paginator.screens = self.ids.logo.screen_names
    
    def createContent(self):

        dpdl = self.dwparser.create_distro_page_data_list(self.distro)
        if len(dpdl) > 0:
            self.createPaginationImage(dpdl[0])
            self.exist = True
            for i in list(dpdl[1]):
                text_1 = i.split(':')[0] + ':'
                text_2 = i.split(':')[1]
                self.ids.distro_info.add_widget(
                    ThreeLineListItem(text=text_1, secondary_text=text_2)
                )
        else:
            self.exist = False

    def back(self, instance):
        self.parent.current = 'girisSayfasi'


if __name__ == '__main__':
    runTouchApp(DistroPage())

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty
from kivy.graphics import Line, Color
from kivymd.uix.card import MDCardPost
from kivymd.uix.label import MDLabel
from kivymd.uix.list import IRightBody, ILeftBody, TwoLineAvatarIconListItem, OneLineListItem
from dwparser import DWParser
from settings import TEMPLATE_DIR
from multiprocessing import Process
import os

kv_file = os.path.join(os.path.join(TEMPLATE_DIR, 'girissayfasi.kv'))
Builder.load_file(kv_file)


class MyListItem(TwoLineAvatarIconListItem):

    link = StringProperty()


class MyOneLineListItem(OneLineListItem):

    link = StringProperty()


class MyMDCardPost(MDCardPost):

    link = StringProperty()


class ListIcon(IRightBody, AsyncImage):
    pass


class ListLabel(ILeftBody, MDLabel):
    pass


class GirisSayfasi(Screen):

    dwparser = DWParser('https://www.distrowatch.com/')
    data = []

    def __init__(self):
        super().__init__()
        self.name = 'girisSayfasi'
        self.listItemHeight = 0
        self.instance_grid_card = self.ids.grid_card
        Process(target=self.addPostCard())
        Process(target=self.addListItem())
        Process(target=self.createSearcPage())

    def callback(self,instance, value):
        
        wrong_link = 'table.php?distribution='
        distro = instance.parent.parent.parent.link
        if wrong_link in distro:
            distro = distro[len(wrong_link):]
        self.parent.openDistroPage(distro)
    
    def refresh_callback(self, *args):

        def refresh_callback(interval):
            self.ids.grid_card.clear_widgets()
            self.addPostCard()
            self.ids.refresh_layout.refresh_done()
            self.tick = 0

        Clock.schedule_once(refresh_callback, 1)

    def addPostCard(self):

        self.data = self.dwparser.create_last_news_data_list('https://www.distrowatch.com/')
        for item in self.data:
            self.instance_grid_card.add_widget(
                    MyMDCardPost(
                        link = item['Link'],
                        source=item['NewsLogo'],
                        tile_text=item['NewsHeadline'],
                        tile_font_style="H5",
                        text_post= item['NewsText'],
                        with_image=True, swipe=False,
                        callback=self.callback
                        ))
        l = self.instance_grid_card.children
        for i in l:
            ind = l.index(i)
            self.instance_grid_card.canvas.add(Color(0.72,0.72,0.72))
            self.instance_grid_card.canvas.add(Line(points=[i.padding[0], i.height*ind + 2*i.padding[0], 
                                                            i.width, i.height*ind + 2*i.padding[0]], 
                                                            width=1))

    def listItemCallBack(self,instance,value):

        if instance.collide_point(value.pos[0],value.pos[1]):
            self.parent.openDistroPage(instance.link)

    def addListItem(self):

        item_list = self.ids.scroll
        data = self.dwparser.create_popularity_data_list()
        for item in data:
            img = ListIcon(source=item['img'])
            text = ListLabel(text=item['phr1'])
            litem = MyListItem(
                    text = item['phr2'],
                    secondary_text = item['phr3'],
                    link = item['phr2link'],
                    on_touch_up = self.listItemCallBack
                    )
            litem.add_widget(img)
            litem.add_widget(text)
            item_list.add_widget(litem)
    
    def searchListItemCallBack(self,instance,value):

        if instance.collide_point(value.pos[0],value.pos[1]):
            self.parent.openDistroPage(instance.link)
            return

    def searchInList(self,keyboard,value):
        
        text = self.ids.search_list_ti.text
        for distro in self.ids.search_list.children:
            if text.lower() in distro.text.lower():
                distro.height = self.listItemHeight
                distro.opacity = 1
            else:
                distro.height = 0
                distro.opacity = 0
        
    def createSearcPage(self):
        
        for distro in self.dwparser.distrolist:
            self.ids.search_list.add_widget(
                MyOneLineListItem(
                    text=distro['name'],
                    link=distro['link'],
                    on_touch_up = self.searchListItemCallBack
                    )
            )
        self.listItemHeight = self.ids.search_list.children[0].height
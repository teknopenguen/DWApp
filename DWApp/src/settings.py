import os
from kivymd.theming import ThemeManager

TM = ThemeManager()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR,'static')
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
SOURCE_DIR = os.path.join(BASE_DIR,'src')
TOOLBARCOLOR = TM.opposite_bg_dark

#bagimliliklar
DEB = [
    'kivy',
    'kivymd',
    'bs4'
]
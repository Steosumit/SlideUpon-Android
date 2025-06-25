from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivymd.app import MDApp


class GridlayoutExample(GridLayout):
    a = "0"
    t = StringProperty("Hello You Clicked !")
    def mybutton(self):
        self.t = "Wow !"
        if  self.a == "6":
            print("Done!")
    def v(self,widget):
        self.a = str(int(widget.value))
        print(str(int(widget.value)) )



class TheLabApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"

    pass



TheLabApp().run()

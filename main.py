import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.boxlayout import BoxLayout

from texte import genere_phrase, finalise_phrase

class TexteApp(App):
    def callback(self, instance):
        self.label.text_size = self.label.size
        self.label.text = finalise_phrase(genere_phrase()['contenu'])
        return

    def build(self):
        box = BoxLayout(orientation='vertical')
        b = Button(text='Klikit warnon')
        self.label = Label(font_size=30)
        self.label.halign = 'center'
        self.label.valign = 'middle'
        box.add_widget(self.label)
        box.add_widget(b)
        b.bind(on_press=self.callback)
        return box

TexteApp().run()

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('robot.kv')

class EyeScreen(Screen):
    mood = NumericProperty(1.0)

    def update_mood(self):
        value = self.ids['moodinput']
        self.mood = value.text
        print 'changing mood'
    
    def switch_image(self, *args):
        eyeimage = self.ids['screenimage']
        print 'hello' + str(eyeimage.source)
        if self.mood < 1.0:
            eyeimage.source = 'eyestest2.png'
        else:
            eyeimage.source = 'eyestest.png'

class MenuScreen(Screen):
    pass

def moodcallback(instance,value):
    print('mood changed to',value)
    instance.switch_image()


sm = ScreenManager()
eyescreen = EyeScreen(name='eyes')
menuscreen = MenuScreen(name='menus')

eyescreen.bind(mood=moodcallback)

sm.add_widget(eyescreen)
sm.add_widget(menuscreen)

#sm.current = 'menus'


class RobotApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    RobotApp().run()


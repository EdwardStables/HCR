from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('robot.kv')

class EyeScreen(Screen):
    pass

class MenuScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(EyeScreen(name='eyes'))
sm.add_widget(MenuScreen(name='menus'))

sm.current = 'menus'

class RobotApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    RobotApp().run()


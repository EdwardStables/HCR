from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.graphics import Rectangle, Color, Ellipse
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import NumericProperty, ReferenceListProperty

Builder.load_file('robot.kv')

class EyeScreen(Screen):
    mood = NumericProperty(1.0) #parameter for updating mood displayed by robot

    def update_mood(self):      #callback for whenever the text box is updated
        value = self.ids['moodinput']
        self.mood = value.text

    def on_mood(self,instance,value):
        leftlid = self.ids['lefteye'].ids['lid']
        rightlid= self.ids['righteye'].ids['lid']
        if value < 1.0:
            leftlid.move_lid(100)
            rightlid.move_lid(100)
        else:
            leftlid.move_lid(0)
            rightlid.move_lid(0)

    def move_look(self,x_change,y_change):
        lefteye = self.ids['lefteye']
        righteye = self.ids['righteye']
        
        lpupil = lefteye.ids['pupil']
        rpupil = righteye.ids['pupil']

        lpupil.target_add(x_change,y_change)
        rpupil.target_add(x_change,y_change)
    
    
class MenuScreen(Screen):
    pass

class EyeImage(Widget):
    pass

class PupilImage(Widget):
    tx = NumericProperty()
    ty = NumericProperty()
    target_pos = ReferenceListProperty(tx,ty)

    def target_add(self,x_change,y_change):
        self.target_pos[0] += x_change
        self.target_pos[1] += y_change
    
    def on_target_pos(self,instance,value):
        if value[0] < self.parent.x:
            self.target_pos[0] = self.parent.x
        elif value[0] > self.parent.x +150:
            self.target_pos[0] = self.parent.x +150
        if value[1] < self.parent.y:
            self.target_pos[1] = self.parent.y
        elif value[1] > self.parent.y +250:
            self.target_pos[1] = self.parent.y +250
        
        anim = Animation(x=self.target_pos[0],y=self.target_pos[1], duration =.2)
        anim.start(self)

class EyelidImage(Widget):
    def move_lid(self,y_drop):
        anim = Animation(size=(self.size[0],-y_drop), duration = 0.1)
        anim.start(self)


sm = ScreenManager()
eyescreen = EyeScreen(name='eyes')
menuscreen = MenuScreen(name='menus')

#eyescreen.bind(mood=moodcallback)
eyescreen.ids['righteye'].ids['pupil'].target_pos=eyescreen.ids['righteye'].ids['pupil'].pos
eyescreen.ids['lefteye'].ids['pupil'].target_pos=eyescreen.ids['lefteye'].ids['pupil'].pos

sm.add_widget(eyescreen)
sm.add_widget(menuscreen)

#sm.current = 'menus'
#eyescreen.mood = 2.0

class RobotApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    RobotApp().run()


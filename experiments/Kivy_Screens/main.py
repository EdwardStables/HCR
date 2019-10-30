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
        print('changing mood')
    
    def switch_image(self, *args):  #whenever the mood is changed update the screen accordingly
        eyeimage = self.ids['lefteye']
        if self.mood < 1.0:
            anim = Animation(x=300, y=100)
            anim.start(eyeimage)
        else:
            anim = Animation(x=100, y=100)
            anim.start(eyeimage)
            
    def move_look(self,x_change,y_change):
        lefteye = self.ids['lefteye']
        righteye = self.ids['righteye']
        
        lpupil = lefteye.ids['pupil']
        rpupil = righteye.ids['pupil']
        
        lpupil.target_pos[0] += x_change
        lpupil.target_pos[1] += y_change
        
        rpupil.target_pos[0] += x_change
        rpupil.target_pos[1] += y_change
        
class MenuScreen(Screen):
    pass

class EyeImage(Widget):
    pass

class PupilImage(Widget):
    tx = NumericProperty()
    ty = NumericProperty()
    target_pos = ReferenceListProperty(tx,ty)

    def move_pupil(self,value,eyepos):
        if value < 1.0:
            newy = eyepos +50
            anim = Animation(x=self.x, y=newy, duration = .2)
            anim.start(self)
        else:
            newy = eyepos
            anim = Animation(x=self.x, y=newy, duration = .2)
            anim.start(self)

    def on_target_pos(self,instance,value):
        anim = Animation(x=value[0],y=value[1], duration =.2)
        anim.start(self)

def moodcallback(instance,value):   #callback for whenever the mood is updated
    print('mood changed to',value)
    right_eye = instance.ids['righteye']
    left_eye = instance.ids['lefteye']
    
    rpupil = right_eye.ids['pupil']
    lpupil = left_eye.ids['pupil']
    
    reye_y = right_eye.y
    leye_y = left_eye.y
    
    rpupil.move_pupil(value,reye_y)
    lpupil.move_pupil(value,leye_y)


sm = ScreenManager()
eyescreen = EyeScreen(name='eyes')
menuscreen = MenuScreen(name='menus')

eyescreen.bind(mood=moodcallback)
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


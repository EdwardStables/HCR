from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider

from kivy.graphics import Rectangle, Color, Ellipse
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import NumericProperty, ReferenceListProperty, BoundedNumericProperty

from kivy.config import Config

Builder.load_file('robot.kv')

Config.set('graphics', 'width', '480')
Config.set('graphics', 'height','320')

class EyeScreen(Screen):
    mood = NumericProperty(0.0) #parameter for updating mood displayed by robot

    def update_mood(self):      #callback for whenever the text box is updated
        value = self.ids['moodinput']
        self.mood = value.text

    def on_mood(self,instance,value):   # put whatever happens on mood change here
        lefttoplid = self.ids['lefteye'].ids['toplid']
        righttoplid= self.ids['righteye'].ids['toplid']

        lefttoplid.open_value=value
        righttoplid.open_value=value

        lefttoplid.open_lid()
        righttoplid.open_lid()

    def move_look(self,x_change,y_change):
        lefteye = self.ids['lefteye']
        righteye = self.ids['righteye']
        
        lpupil = lefteye.ids['pupil']
        rpupil = righteye.ids['pupil']

        lpupil.target_add(x_change,y_change)
        rpupil.target_add(x_change,y_change)

    def set_look(self,x_target,y_target): #give input as a value betewen 0 and 1 for relative positions
        lefteye = self.ids['lefteye']
        righteye = self.ids['righteye']
        
        lpupil = lefteye.ids['pupil']
        rpupil = righteye.ids['pupil']

        rpupil.target_set(x_target,y_target)
        lpupil.target_set(x_target,y_target)
    
class EyeImage(Widget):
    pass

class PupilImage(Widget):
    tx = BoundedNumericProperty(0, min=-1, max=1,errorhandler=lambda x: 1 if x > 1 else -1)
    ty = BoundedNumericProperty(-1, min=-1, max=1,errorhandler=lambda x: 1 if x > 1 else -1)
    target_pos = ReferenceListProperty(tx,ty)

    def target_add(self,x_change,y_change):
        self.target_pos[0] += x_change
        self.target_pos[1] += y_change
    
    def on_target_pos(self,instance,value):
        print('updating pupil pos'+str(value))
        print(str(self.parent.y)+','+str(self.target_pos[0])+','+str(self.size[0]))
        abs_x = self.parent.x + 0.5*(1+self.target_pos[0])*(self.parent.size[0]-self.size[0]) 
        abs_y = self.parent.y + 0.5*(1+self.target_pos[1])*(self.parent.size[1]-0.7*self.size[1]+self.parent.ids['toplid'].size[1]) 
        print(str(abs_x) + "," + str(abs_y))
        anim = Animation(x=abs_x,y=abs_y, duration =.05)
        anim.start(self)


    def check_pos(self,dist):
        abs_x = self.parent.x + 0.5*(1+self.target_pos[0])*(self.parent.size[0]-self.size[0]) 
        abs_y = self.parent.y + 0.5*(1+self.target_pos[1])*(self.parent.size[1]-0.7*self.size[1]+dist) 
        anim = Animation(x=abs_x,y=abs_y, duration =.05)
        anim.start(self)

class TopEyelidImage(Widget):
    open_value = BoundedNumericProperty(0, min=-1, max=1,errorhandler=lambda x: 1 if x > 1 else -1)
    
    def open_lid(self):
        dist = -(self.open_value*(self.parent.size[1]-0.7*self.parent.ids['pupil'].size[0]))
        self.parent.ids['pupil'].check_pos(dist)
        anim = Animation(size=(self.size[0],dist), duration = 0.01)
        anim.start(self)

    def close_lid(self):
        anim = Animation(size=(self.size[0],-self.parent.size[1]), duration = 0.01)
        anim.start(self)

class BotEyelidImage(Widget):
    open_value = BoundedNumericProperty(0, min=-1, max=1,errorhandler=lambda x: 1 if x > 1 else -1)
    
    def open_lid(self):
        dist = (0.5*self.open_value*(self.parent.size[1]-0.7*self.parent.ids['pupil'].size[0]))
        self.parent.ids['pupil'].check_pos(dist)
        anim = Animation(size=(self.size[0],dist), duration = 0.01)
        anim.start(self)

    def close_lid(self):
        anim = Animation(size=(self.size[0],-self.parent.size[1]), duration = 0.01)
        anim.start(self)

class MenuScreen(Screen):
    pass

class VotingScreen(Screen):
    def pass_reaction(self,reaction):       #placeholder for now, will change later
        print("user reacted with : "+str(reaction))

sm = ScreenManager()
eyescreen = EyeScreen(name='eyes')
menuscreen = MenuScreen(name='menus')
votingscreen=VotingScreen(name='voting')
print(str(sm.size))

sm.add_widget(eyescreen)
sm.add_widget(menuscreen)
sm.add_widget(votingscreen)

class RobotApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    RobotApp().run()


from hcrutils.subsystem import subsystem
from hcrutils.message import messagebody

from os import path
from functools import partial

from kivy.app import App

from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider
from kivy.uix.button import Button

from kivy.graphics import Rectangle, Color, Ellipse
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, BoundedNumericProperty

from kivy.config import Config


class screen(subsystem):

    def __init__(self, root_path):
        super().__init__("screen", "id_only")
        self.root_path = root_path

    def _run(self):
        Builder.load_file(path.join(self.root_path, 'screen_subsystem/robot.kv'))

        Config.set('graphics', 'width', '480')
        Config.set('graphics', 'height','320')
        Config.set('graphics', 'borderless', '1')

        RobotApp(self).run()


class EyeScreen(Screen):
    mood = NumericProperty(0.0) #parameter for updating mood displayed by robot

    def update_mood(self):      #callback for whenever the text box is updated
        value = self.ids['moodinput']
        self.mood = value.text

    def on_mood(self,instance,value):   # put whatever happens on mood change here
        lefttoplid = self.ids['lefteye'].ids['toplid']
        righttoplid= self.ids['righteye'].ids['toplid']
        leftbotlid = self.ids['lefteye'].ids['bottomlid']
        rightbotlid= self.ids['righteye'].ids['bottomlid']

        lefttoplid.open_value=value
        righttoplid.open_value=value
        leftbotlid.open_value=value
        rightbotlid.open_value=value

        lefttoplid.open_lid()
        righttoplid.open_lid()
        leftbotlid.open_lid()
        rightbotlid.open_lid()
        
    def move_look(self,x_change,y_change):
        lefteye = self.ids['lefteye']
        righteye = self.ids['righteye']
        
        lpupil = lefteye.ids['pupil']
        rpupil = righteye.ids['pupil']

        lpupil.target_add(x_change,y_change)
        rpupil.target_add(x_change,y_change)

    def set_look(self,x_target,y_target): #give input as a value betewen 0 and 1 for relative positions
        x_target = round(x_target, 2)
        y_target = round(y_target, 2)

        lpupil = self.ids['lefteye'].ids['pupil']
        rpupil = self.ids['righteye'].ids['pupil']

        lpupil.target_set(x_target,y_target)
        rpupil.target_set(x_target,y_target)
    
class EyeImage(Widget):
    pass

class PupilImage(Widget):
    tx = BoundedNumericProperty(0, min=-1, max=1,errorhandler=lambda x: 1 if x > 1 else -1)
    ty = BoundedNumericProperty(-1, min=-1, max=1,errorhandler=lambda x: 1 if x > 1 else -1)
    target_pos = ReferenceListProperty(tx,ty)

    def target_add(self,x_change,y_change):
        self.target_pos[0] += x_change
        self.target_pos[1] += y_change

    def target_set(self,x_target,y_target):
        self.target_pos[0] = x_target
        self.target_pos[1] = y_target
    
    def on_target_pos(self,instance,value):
        self.get_abs_pos(self.parent.ids['toplid'].size[1],self.parent.ids['bottomlid'].size[1])

    def get_abs_pos(self,disttop,distbot):
        abs_x = self.parent.x + 0.5*(1+self.target_pos[0])*(self.parent.size[0]-self.size[0]) 
        abs_y = self.parent.y + 0.5*(1+self.target_pos[1])*(self.parent.size[1]-self.size[1])
        if(abs_y>self.parent.y+self.parent.size[1]+self.parent.ids['toplid'].size[1]-0.7*self.size[1]):
            abs_y=self.parent.y+self.parent.size[1]+self.parent.ids['toplid'].size[1]-0.7*self.size[1]
        elif (abs_y<self.parent.y+self.parent.ids['bottomlid'].size[1]-0.3*self.size[1]):
            abs_y=self.parent.y+self.parent.ids['bottomlid'].size[1]-0.3*self.size[1]
        #print(str(abs_x) + "," + str(abs_y))
        anim = Animation(x=abs_x,y=abs_y, duration =.1)
        anim.start(self)

class TopEyelidImage(Widget):
    open_value = BoundedNumericProperty(0, min=-1, max=1,errorhandler=lambda x: 1 if x > 1 else -1)
    
    def open_lid(self):
        dist = -(self.open_value*(self.parent.size[1]-0.7*self.parent.ids['pupil'].size[0]))
        self.parent.ids['pupil'].get_abs_pos(dist,self.parent.ids['bottomlid'].size[1])
        anim = Animation(size=(self.size[0],dist), duration = 0.01)
        anim.start(self)

    def close_lid(self):
        anim = Animation(size=(self.size[0],-self.parent.size[1]), duration = 0.01)
        anim.start(self)

class BotEyelidImage(Widget):
    open_value = BoundedNumericProperty(0, min=-1, max=1,errorhandler=lambda x: 1 if x > 1 else -1)
    
    def open_lid(self):
        dist = -(0.5*self.open_value*(self.parent.size[1]-0.7*self.parent.ids['pupil'].size[0]))
        self.parent.ids['pupil'].get_abs_pos(self.parent.ids['toplid'].size[1],dist)
        anim = Animation(size=(self.size[0],dist), duration = 0.01)
        anim.start(self)

    def close_lid(self):
        anim = Animation(size=(self.size[0],-self.parent.size[1]), duration = 0.01)
        anim.start(self)

class VotingButton(Button):
    value = NumericProperty(0)

class MenuScreen(Screen):
    pass

class VotingScreen(Screen):
    def pass_reaction(self,reaction):       
        #placeholder for now, will change later
        pass
    def to_eyes(self):
        self.manager.transition.direction='down'
        self.manager.current = 'eyes'

class RobotScreens(ScreenManager):
    pass

class RobotApp(App):
    def __init__(self, op):
        self.op = op
        super().__init__()

    @staticmethod
    def message_callback(ref, *largs):
        #Returns the normalized position of the largest face 
        eye_pos = ref.op.get_messages("rel_faces")
        if eye_pos:
            p = eye_pos[0].message
            ref.eyescreen.set_look(float(p[0]), float(p[1]))

        #Add more in the same way...

    def build(self):
        sm = RobotScreens()
        #self.eyescreen = EyeScreen(name='eyes')
        #self.menuscreen = MenuScreen(name='menus')
        #self.votingscreen=VotingScreen(name='voting')

        #sm.add_widget(self.eyescreen)
        #sm.add_widget(self.menuscreen)
        #sm.add_widget(self.votingscreen)

        message_event = Clock.schedule_interval(
            partial(self.message_callback, self), 0.01)

        return sm



# Resolution - 800x480
from kivy.app import App
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import ListProperty
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from extron_serial import Extron

# Just for testing - remove in practice
# from kivy.core.window import Window
# Window.size = (800, 480)
switcher = Extron()


class Interface(BoxLayout):
    """
    Class widget representing the screen layout.
    """
    pass

class Toggles(GridLayout):
    pass

class BlankToggle(ToggleButton):
    def __init__(self, **kwargs):
        super(BlankToggle, self).__init__(**kwargs)
        self.last_color = 0, 0, 0, 1
        
    def on_state(self, widget, value):
        if value == 'down':
            switcher.blank()
            self.last_color = self.background_color
            self.background_color = 51/255, 0, 111/255, 0.8
            self.text = 'Unblank'
        else:
            switcher.unblank()
            self.background_color = self.last_color
            self.text = 'Blank'
    
class FreezeToggle(ToggleButton):
    """
    Class representing freeze button, goes inside Interface.
    """
    def __init__(self, **kwargs):
        super(FreezeToggle, self).__init__(**kwargs)
        self.last_color = 0, 0, 0, 0

    def on_state(self, widget, value):
        if value == 'down':
            switcher.freeze()
            self.last_color = self.background_color
            self.background_color = 51/255, 0, 111/255, 0.8
            self.text = 'Unfreeze'
        else:
            switcher.unfreeze()
            self.background_color = self.last_color
            self.text = 'Freeze'
            
  
class InputToggle(ToggleButton):
    """
    Class representing input select buttons - goes inside InputPanel.
    """
    background_color_normal = ListProperty([0, 0, 0, 0])
    background_color_down = ListProperty([0, 0, 0, 0])
    color_down = ListProperty()
    color_normal = ListProperty()

    def __init__(self, **kwargs):
        super(InputToggle, self).__init__(**kwargs)

    def on_state(self, widget, value):
        if value == 'down':
            switcher.select_input(self.output)
            self.background_color = self.background_color_down
            self.color = self.color_down
            self.bold = True
            with self.canvas.after:
                Color(233/255, 60/255, 172/255, 0.9)
                Line(width=2, rectangle=[self.x, self.y,
                                self.width, self.height])
        else:
            self.background_color = self.background_color_normal
            self.color = self.color_normal
            self.bold = False
            self.canvas.after.clear()

    
class InputPanel(GridLayout):
    """
    Class Representing panel of input buttons - goes inside Interface.
    """
    pass
    
class HuskyLabel(Label):
    pass
    
class MuteButton(ToggleButton):
    def on_state(self, widget, value):
        if value == 'down':
            self.last_color = self.background_color
            self.background_color = 51/255, 0, 111/255, 0.8
            switcher.mute()
            self.text = 'Unmute'
        else:
            self.background_color = self.last_color
            switcher.unmute()
            self.text = 'Mute'
    
class PowerToggle(ToggleButton):
    background_color_normal = ListProperty([0, 0, 0, 0])
    background_color_down = ListProperty([0, 0, 0, 0])
    def __init__(self, **kwargs):
        super(PowerToggle, self).__init__(**kwargs)

    def on_state(self, widget, value):
        if value == 'down':
            switcher.turn_projector_on()
            self.background_color = self.background_color_down
            self.text = 'Turn Projector Off'
        else:
            switcher.turn_projector_off()
            self.background_color = self.background_color_normal
            self.text = 'Turn Projector On'

class VolumeSlider(Slider):
    """
    Class representing volume slider. Goes inside Interface.
    """
    def __init__(self, **kwargs):
        super(VolumeSlider, self).__init__(**kwargs)

    def on_touch_up(self, touch):
        volume = int(-1 * (95 + (-100 / (1 + pow(1.5, (-0.2 * (self.value - 65)))))))
        switcher.set_volume(volume)
        print(f"Volume set to {str(volume)}" )

class HuskontrollerApp(App):
    """
    Actual app class for Kivy.
    """
    def build(self):
        return Interface()

if __name__ == '__main__':
	HuskontrollerApp().run()
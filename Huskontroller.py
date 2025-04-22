# Resolution - 800x480
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle
from kivy.lang.builder import Builder
from kivy.properties import ListProperty
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

# Use this in testing - remove in production
# Window.size = (800, 480)
Window.show_cursor = False

# Use this in production

Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'borderless', '1')
Builder.load_file('Huskontroller.kv')

# Disable the following if using the test_serial.py module 
from extron_serial import Extron
switcher = Extron()

# Enable the following to use the test_serial.py module
#from test_serial.py import TestDevice
#switcher = TestDevice()

class Interface(BoxLayout):
    """
    Class widget representing the screen layout as a whole.
    """
    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)

        freeze_toggle = FreezeToggle()
        blank_toggle = BlankToggle()

        power_toggle = PowerToggle(freeze_toggle=freeze_toggle,
                                 blank_toggle=blank_toggle)

        self.add_widget(freeze_toggle)
        self.add_widget(blank_toggle)
        self.add_widget(power_toggle)


class Toggles(GridLayout):
    """
    Class storing the area where the Toggle buttons are used.
    """
    pass

class BlankToggle(ToggleButton):
    """
    Class representing the Blank toggle button.
    """
    def __init__(self, **kwargs):
        super(BlankToggle, self).__init__(**kwargs)
        
    def on_state(self, widget, value):
        if value == 'down':
            switcher.blank()
            self.background_color = self.background_color_down
            self.color = self.color_down
            self.text = 'Unblank'
        else:
            switcher.unblank()
            self.background_color = self.background_color_normal
            self.color = self.color_normal
            self.text = 'Blank'

class DisplayStatePanel(BoxLayout):
    pass

class FreezeToggle(ToggleButton):
    """
    Class representing freeze button.
    """
    def __init__(self, **kwargs):
        super(FreezeToggle, self).__init__(**kwargs)

    def on_state(self, widget, value):
        if value == 'down':
            switcher.freeze()
            self.background_color = self.background_color_down
            self.color = self.color_down
            self.text = 'Unfreeze'
        else:
            switcher.unfreeze()
            self.background_color = self.background_color_normal
            self.color = self.color_normal
            self.text = 'Freeze'
            
  
class InputToggle(ToggleButton):
    """
    Class representing input select buttons.
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
            with self.canvas.after:
                Color(233/255, 60/255, 172/255, 0.9)
                Line(width=2, rectangle=[self.x, self.y,
                                self.width, self.height])
        else:
            self.background_color = self.background_color_normal
            self.color = self.color_normal
            self.canvas.after.clear()

    
class InputPanel(GridLayout):
    """
    Class Representing panel of input buttons.
    """
    pass
    
class HuskyLabel(Label):
    """
    Represents the Husky Label - this isn't actually used currently.
    """
    pass

class MuteButton(ToggleButton):
    """
    Represents the mute button.
    """
    def on_state(self, widget, value):
        if value == 'down':
            self.background_color = self.background_color_down
            self.color = self.color_down
            switcher.mute()
            self.text = 'Unmute'
        else:
            self.background_color = self.background_color_normal
            self.color = self.color_normal
            switcher.unmute()
            self.text = 'Mute'

class PowerOnMessage(Popup):
    """
    Class producing a 10-second countdown message when the projector power button
    is toggled via PowerToggle.
    """
    def __init__(self, **kwargs):
        super(PowerOnMessage, self).__init__(**kwargs)
        self.seconds = 10
        self.message = Label(text=f"Interface available in {self.seconds} seconds...", font_size='24sp')
        self.content = self.message
        
        Clock.schedule_interval(self.update_timer, 1)
    
    def update_timer(self, seconds):
        self.seconds -= 1
        if self.seconds == 0:
            self.dismiss()
        else:
            self.message.text = f"Interface available in {self.seconds} seconds..."

    
class PowerToggle(ToggleButton):
    """
    Class representing the power toggle button for the projector.
    """
    background_color_normal = ListProperty([0, 0, 0, 0])
    background_color_down = ListProperty([0, 0, 0, 0])
    def __init__(self, freeze_toggle=None,
                 blank_toggle=None, **kwargs):
        super(PowerToggle, self).__init__(**kwargs)
        self.freeze_toggle = freeze_toggle
        self.blank_toggle = blank_toggle

    def on_state(self, widget, value):
        if value == 'down':
            switcher.turn_projector_on()
            self.background_color = self.background_color_down
            self.color = self.color_down
            self.text = 'Turn Projector Off'
            message = PowerOnMessage()
            message.open()
            
            if self.freeze_toggle:
                self.freeze_toggle.state = 'normal'
            if self.blank_toggle:
                self.blank_toggle.state = 'normal'
        else:
            switcher.turn_projector_off()
            self.background_color = self.background_color_normal
            self.color = self.color_normal
            self.text = 'Turn Projector On'

class VolumeSlider(Slider):
    """
    Class representing volume slider.
    """
    
    def __init__(self, **kwargs):
        super(VolumeSlider, self).__init__(**kwargs)
        self.touched = False
    
    def on_touch_down(self, touch):
        """
        Marks the volume control as "touched" on touch down. The touched
        flag is consumed by a touch_up event if the touch_up occurs inside
        the volume slider's area.
        """
        super().on_touch_down(touch)
        if self.collide_point(*touch.pos):
            self.touched = True

    def on_touch_up(self, touch):
        """
        Sets the volume to a linear value between 0 and -50 based on the location selected
        on the volume control bar.
        
        Consumes the "touched" flag created by on_touch_down() for this class.
        """
        if (self.touched):
            volume = int(self.value / 2 - 50)
            switcher.set_volume(volume)
            print(f"Volume set to {str(volume)}" )
            self.touched = False

class HuskontrollerApp(App):
    """
    Actual app class for Kivy.
    """
    def build(self):
        return Interface()

if __name__ == '__main__':
    """
    Kivy expects an <Appname>App().run() call to start any given Kivy app.
    """
    HuskontrollerApp().run()

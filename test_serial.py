class TestDevice:
    def __init__(self):
    """
    Prints that the test device is enabled.
    This entire module is used to test the sent commands of
    the Huskontroller software by sending the commands to the
    terminal console. It's good for proto-typing new hardware
    commands for copying into production code or testing changes
    to the interface.
    """
        print(f'Test device enabled.')
    
    def send_command(self, command):
        """
        Takes a string "command". Typically would send the command as an
        encoded byte string, but in this case, just prints to the console.
        """
        print("Sent command: " + command)
    
    def select_input(self, input_device):
        inputs = {'podium': '1!', 'hdmi': '2!', 'usb-c': '3!', 'vga': '4!'}
        command = inputs[input_device]
        self.send_command(command)
    
    def freeze(self):
        self.send_command('1*1F')
        
    def unfreeze(self):
        self.send_command('1*0F')
    
    def blank(self):
        self.send_command('1*1B')
    
    def unblank(self):
        self.send_command('1*0B')
        
    def turn_projector_on(self):
        self.send_command('W+snds9*9|%02PON%03')
    
    def turn_projector_off(self):
        self.send_command('W+snds9*9|%02POF%03')
    
    def set_volume(self, volume_level):
        command = str(volume_level) + 'V'
        self.send_command(command)
    
    def mute(self):
        self.send_command('1Z')
    
    def unmute(self):
        self.send_command('0Z')
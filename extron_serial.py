import serial
from serial.tools import list_ports

class Extron:
    def __init__(self):
        try:
            port_list = list_ports.comports()
            port_names = []
            for port in port_list:
                port_names += port
            self.extron_device = serial.Serial('COM3', 9600)
            print(f'Device {self.extron_device} created.')
        except serial.SerialException:
            print(f'Error opening connection to port: {port_list[0]}')
        self.current_volume = -10
    
    def send_command(self, command):
        print("Sent command: " + command)
        #self.extron_device.write(command.encode())
    
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
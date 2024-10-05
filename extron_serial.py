import logging
import serial
from pathlib import Path
from serial.tools import list_ports

class Extron:
    def __init__(self):
        """
        Initializes device - gets a list of all connected
        serial devices, picking the first from the list and assuming
        that's the Extron device. If multiple serial devices are
        connected, modify this to account for the devices.
        """
        self.logger = logging.getLogger('extron_serial')
        self.logger.setLevel(logging.DEBUG)
        
        log_path = Path('logs')
        if not log_path.exists():
            log_path.mkdir()
        file_handler = logging.FileHandler('logs/extron_serial.log')
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(fmt='%(asctime)s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.info('Extron serial device connection initializing...\n')
        
        try:
            port_list = list_ports.comports()
            port_names = []
            for port in port_list:
                port_names += port
            self.extron_device = serial.Serial(port_names[0], 9600)
            self.logger.info(f'Device {self.extron_device} created.')
        except serial.SerialException:
            self.logger.error(f'Error opening connection to port: {port_list[0]}')
        self.current_volume = -25
    
    def send_command(self, command):
        """
        Takes a command string and sends the command as an
        encoded byte string to the Extron device.
        """
        self.logger.info(f'Sending command: {command}')
        self.extron_device.write(command.encode())
    
    def select_input(self, input_device):
        """
        Takes the name of an input device 'podium', 'hdmi', 'usb-c', or 'vga'
        and sends the associated command to the Extron switcher.
        """
        inputs = {'podium': '1!', 'hdmi': '2!', 'usb-c': '3!', 'vga': '4!'}
        command = inputs[input_device]
        self.send_command(command)
    
    def freeze(self):
        """
        Sends the Extron command necessary for 
        """
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

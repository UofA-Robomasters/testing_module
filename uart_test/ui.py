import serial
import Tkinter
import threading

Port = '/dev/ttyTHS2'

class SerialDebugger:
    def __init__(self):
        self.top = Tkinter.Tk()
        self.top.title('Serial Debugger for DJI Manifold')
        # self.top.geometry('500x400')
        self.top.resizable(width=False, height=False)

        self.settingFrame = Tkinter.Frame(self.top)
        self.settingFrame.pack(side='top', padx=10, pady=5)
        self.bitrateLabel = Tkinter.Label(self.settingFrame, text='Bitrate')
        self.bitrateLabel.pack(side='left')
        self.bitrateText = Tkinter.Text(self.settingFrame, height=1, width=10)
        self.bitrateText.pack(side='left', padx=10, pady=5)
        self.startButton = Tkinter.Button(
                self.settingFrame, text='Start', command=self.start_serial)
        self.startButton.pack(side='left', padx=10, pady=5)
        self.stopButton = Tkinter.Button(
                self.settingFrame, text='Stop', command=self.stop_serial)
        self.stopButton.pack(side='left', padx=10, pady=5)
        self.stopButton['state'] = 'disabled'

        self.msgFrame = Tkinter.Frame(self.top)
        self.msgFrame.pack(side='top', padx=10, pady=5)
        self.sendMsgText = Tkinter.Text(self.msgFrame, height=1, width=20)
        self.sendMsgText.pack(side='left', padx=10, pady=5)
        self.sendOnceButton = Tkinter.Button(
                self.msgFrame, text='Send Once', command=self.send_once)
        self.sendOnceButton.pack(side='left', padx=10, pady=5)
        self.sendRepeatButton = Tkinter.Button(
                self.msgFrame, text='Send Repeat', command=self.send_repeat)
        self.sendRepeatButton.pack(side='left', padx=10, pady=5)
        self.stopSendButton = Tkinter.Button(
                self.msgFrame, text='Stop Sending', command=self.stop_send)
        self.stopSendButton.pack(side='left', padx=10, pady=5)
        self.incomeMsgText = Tkinter.Text(self.top, height=25, width=55)
        self.incomeMsgText.pack(side='top', padx=10, pady=5)

        self.sendOnceButton['state'] = 'disabled'
        self.sendRepeatButton['state'] = 'disabled'
        self.stopSendButton['state'] = 'disabled'

        self.ser = None

        self.top.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.top.mainloop()

    def start_serial(self):
        bitrate = int(self.bitrateText.get('1.0', 'end-1c'))
        self.ser = serial.Serial(Port, bitrate, timeout=0.1)
        self.bitrateText['state'] = 'disabled'
        self.stopButton['state'] = 'normal'
        self.startButton['state'] = 'disabled'
        self.sendOnceButton['state'] = 'normal'
        self.sendRepeatButton['state'] = 'normal'
        self.receiving = True
        self.receiving_thread = threading.Thread(target=self.read_serial, args=[])
        self.receiving_thread.daemon = True
        self.receiving_thread.start()
        print 'Port {} opened successfully with bitrate {}'.format(Port, bitrate)

    def read_serial(self):
        print 'Receiving started'
        while self.receiving:
            msg = self.ser.read(1)
            if len(msg) == 1:
                self.incomeMsgText.insert('1.0', str(ord(msg) + '\n'))
        print 'Receiving stopped'

    def stop_serial(self):
        self.receiving = False
        self.ser.close()
        self.ser = None
        self.stopButton['state'] = 'disabled'
        self.bitrateText['state'] = 'normal'
        self.startButton['state'] = 'normal'
        self.sendOnceButton['state'] = 'disabled'
        self.sendRepeatButton['state'] = 'disabled'
        print 'Communication stopped'

    def send_once(self):
        msg = self.sendMsgText.get('1.0', 'end-1c')
        if msg != '':
            msg = msg.strip().split()
            msg = bytearray([int(x) for x in msg])
            self.ser.write(msg)
            print 'Message sent'

    def send_repeat(self):
        msg = self.sendMsgText.get('1.0', 'end-1c')
        if msg != '':
            msg = msg.strip().split()
            msg = bytearray([int(x) for x in msg])
            self.sendOnceButton['state'] = 'disabled'
            self.stopSendButton['state'] = 'normal'
            self.sendRepeatButton['state'] = 'disabled'
            self.sending = True
            self.sending_thread = threading.Thread(target=self.send_serial, args=[msg])
            self.sending_thread.daemon = True
            self.sending_thread.start()
            print 'Repeated sending started'

    def send_serial(self, msg):
        while self.sending:
            self.ser.write(msg)
            print 'Message sent'
        print 'Repeated sending stopped'

    def stop_send(self):
        self.sending = False
        self.stopSendButton['state'] = 'disabled'
        self.sendOnceButton['state'] = 'normal'
        self.sendRepeatButton['state'] = 'normal'

    def on_closing(self):
        if self.ser != None:
            self.ser.close()
        self.top.destroy()

if __name__ == '__main__':
    sd = SerialDebugger()

import tkinter as tk
from tkinter import ttk
from serial import Serial
from serial.tools import list_ports

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        master.title('Redox controls')
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.serial = Serial()
        self.scales = []
        self.ports = list(map(lambda port: port.name, list_ports.comports()))

        label = ttk.Label(self, text="Select port")
        label.grid(row=0, columnspan=3)
        self.portSelector = ttk.Combobox(self, values=self.ports)
        self.portSelector.grid(row=1, column=0, sticky=tk.W, padx=5)

        self.connectButton = tk.Button(self, command=self.connect_to_port, text="Connect")
        self.connectButton.grid(row=1, column=1, sticky=tk.E, padx=5)

        self.refreshButton = tk.Button(self, command=self.update_port_list, text="Refresh")
        self.refreshButton.grid(row=1, column=2, sticky=tk.E, padx=5)

        for peripheral in ['Pump', 'Stirrer', 'LED']:
          self.create_scale(peripheral)

    def update_port_list(self):
      self.ports = list(map(lambda port: port.name, list_ports.comports()))
      self.portSelector.set('')
      self.portSelector['values'] = self.ports

    def connect_to_port(self):
      port = self.portSelector.get()
      self.serial.port = port
      try: 
        self.serial.open()
        for scale in self.scales:
          scale['state'] = 'normal'
      except:
        pass
    
    def create_scale(self, peripheralName):
      scale = tk.Scale(self, from_=0, to=100, label=peripheralName, orient=tk.HORIZONTAL, length = 300, command=self.create_serial_sender(peripheralName[:1]))
      scale.grid(columnspan=3)
      scale['state'] = 'disabled'
      self.scales.append(scale)

    def create_serial_sender(self, commandID):
      return lambda num: self.serial.write(bytes(commandID + num + '\n', 'ascii'))

    def destroy(self):
      try:
        for cmd in ['P', 'L', 'S']:
          self.serial.write(bytes(cmd + '0\n', 'ascii'))
      except:
        pass
      return super().destroy()


root = tk.Tk()
myapp = App(root)
myapp.mainloop()
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
        self.is_connected = False

        label = ttk.Label(self, text="Select port")
        label.grid(row=0, columnspan=3)
        self.portSelector = ttk.Combobox(self, values=self.ports)
        self.portSelector.grid(row=1, column=0, sticky=tk.W, padx=5)

        self.connectButton = tk.Button(
            self, command=self.toggle_connection, text="Connect")
        self.connectButton.grid(row=1, column=1, sticky=tk.E, padx=5)

        self.refreshButton = tk.Button(
            self, command=self.update_port_list, text="Refresh")
        self.refreshButton.grid(row=1, column=2, sticky=tk.E, padx=5)

        for peripheral in ['Pump', 'Stirrer']:
            self.create_scale(peripheral)

    def update_port_list(self):
        self.disconnect_from_port()
        self.ports = list(map(lambda port: port.name, list_ports.comports()))
        self.portSelector.set('')
        self.portSelector['values'] = self.ports

    def toggle_connection(self):
        if self.is_connected:
            self.disconnect_from_port()
        else:
            self.connect_to_port()

    def connect_to_port(self):
        port = self.portSelector.get()
        self.serial.port = port
        try:
            self.serial.open()
            for scale in self.scales:
                scale['state'] = 'normal'
            self.connectButton.configure(text="Disconnect")
            self.is_connected = True
        except:
            pass

    def disconnect_from_port(self):
        try:
            self.reset_all_values()
            self.serial.close()
            self.is_connected = False
            self.connectButton.configure(text="Connect")
        except:
            pass

    def create_scale(self, peripheralName):
        scale = tk.Scale(self, from_=0, to=100, label=peripheralName, orient=tk.HORIZONTAL,
                         length=300, command=self.create_serial_sender(peripheralName[:1]))
        scale.grid(columnspan=3)
        scale['state'] = 'disabled'
        self.scales.append(scale)

    def create_serial_sender(self, commandID):
        return lambda num: self.serial.write(bytes(commandID + num + '\n', 'ascii'))

    def reset_all_values(self):
        for cmd in ['P', 'L', 'S']:
            self.serial.write(bytes(cmd + '0\n', 'ascii'))

    def destroy(self):
        self.disconnect_from_port()
        return super().destroy()


root = tk.Tk()
myapp = App(root)
myapp.mainloop()

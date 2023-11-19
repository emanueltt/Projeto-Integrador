import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
from threading import Thread
from tkinter import *
import customtkinter as CT

"""
TODO:
- Botão Iniciar Experimento: aciona o motor
- Botão Direção: mudar o sentido da corrente pela ponte H, para tracionar ou soltar
- Botão Configurar Tempo de Experimento: (talvez mostrar barra de progressão) por ex.: 10 segundos, depois
disso desligar o motor
- Botão Calibrar: envia comando pro algoritmo de CV para calibrar os pixels
- Botão Focar Câmera: envia comando pro terminal que configura o foco da câmera
- Checar por que a medição do sensor não tá certa

ProgressBar
"""

# Constantes
__arduino__ = True # Set to false when Arduino not connected
arduino_port = '/dev/ttyACM0'
baud_rate = 9600
thread_delay = 500 # ms
y_min = 0
y_max = 100 # [%]
CT.set_appearance_mode("dark")
CT.set_default_color_theme("green")

class Interface:
    def __init__(self) -> None:        
        if __arduino__: 
            self.arduino = serial.Serial(arduino_port, baud_rate)
        self.sensor_readings = []
        self.running = False
        self.time = 0
        self.dir = 0 # 0 -> esquerda, 1 -> direita
    
    def start(self) -> None:
        print("Iniciando experimento...")
        print("Acionando motor...")
        self.clean_all()
        self.running = True
        read_thread.start()

    def change_dir(self) -> None:
        print("Direção de movimento alterada")
        self.dir = switch.get()

    def set_time(self) -> None:
        dialog = CT.CTkInputDialog(text="Tempo de ensaio:", title="Configurar Tempo de Experimento")
        try:
            self.time = int(dialog.get_input())
            print("Tempo de Experimento configurado")
        except Exception as e:
            print("[ERROR] ", e)

    def calibrate(self) -> None:
        print("Algoritmo calibrado")

    def focus(self) -> None:
        print("Focando câmera...")
    
    def read_sensor(self) -> None:
        # while True:
        for i in range(self.time):
            # print("Reading sensor values")
            if(self.running):
                try:
                    value = self.arduino.readline().strip().decode('utf-8')
                    print("value: ", value)
                    self.sensor_readings.append(value)
                except Exception as e:
                    print("[ERROR] ", e)
                    pass
    
    def create_plot(self) -> None:
        canvas_frame = CT.CTkFrame(frame)
        canvas_frame.grid(row=len(buttons) // 3 + 1, columnspan=2, pady=10)
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_ylim([y_min, y_max])
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        
    def update_plot(self) -> None:
        self.ax.clear()
        self.ax.plot(self.sensor_readings, color='green', linewidth=2, marker='o', markersize=5, label='Leitura do Sensor')
        self.ax.set_xlabel('Tempo')
        self.ax.set_ylabel('Sensor')
        self.ax.set_title('Leitura do Sensor em Tempo Real')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.legend(loc='upper right')
        self.canvas.draw()
        root.after(thread_delay, self.update_plot)

    def clean_all(self) -> None:
        self.sensor_readings = []

if __name__ == "__main__":
    interface = Interface()

    # Thread para fazer leitura da serial do Arduino
    read_thread = Thread(target=interface.read_sensor)
    read_thread.daemon = True

    root = CT.CTk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.geometry(f"{screen_width}x{screen_height}")
    root.title("Interface Ensaio de Tração")

    frame = CT.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill=BOTH, expand=True)

    button_texts = [
        'Iniciar experimento',
        'Configurar Tempo de Experimento',
        'Calibrar algoritmo',
        'Focar câmera'
    ]

    button_commands = [
        interface.start,
        interface.set_time,
        interface.calibrate,
        interface.focus,
    ]

    buttons = [CT.CTkButton(frame, text=text, width=200, height=60, command=cmd) 
               for text, cmd in zip(button_texts, button_commands)]

    for i, button in enumerate(buttons):
        row = i // 3
        col = i % 3
        button.grid(row=row, column=col, padx=20, pady=20)

    for i in range(3):
        frame.columnconfigure(i, weight=1)

    switch = CT.CTkSwitch(master=frame, text="Mudar sentido", command=interface.change_dir)
    switch.grid(row=1, column=1, padx=10, pady=10)

    interface.create_plot()
    root.after(thread_delay, interface.update_plot)

    plot_button = CT.CTkButton(frame, text="Limpar", command=interface.clean_all)
    plot_button.grid(row=len(buttons) // 3, column=2, pady=10)

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(len(buttons) // 3 + 1, weight=1)

    progressbar = CT.CTkProgressBar(frame)
    progressbar.grid(row=len(buttons) // 3 + 1, column=2, padx=60, pady=10, sticky="ew")
    progressbar.configure(mode="determinate")
    progressbar.set(0.2)

    root.mainloop()
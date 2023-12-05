import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
from threading import Thread
from tkinter import *
import tkinter.messagebox as MessageBox
import customtkinter as CT
import os
import time

# Constantes
__arduino__ = False # False quando o Arduino não tiver conectado
arduino_port = '/dev/ttyACM0'
baud_rate = 9600
thread_delay = 500 # ms
y_min = 0
y_max = 100 # [%]
CT.set_appearance_mode("dark")
CT.set_default_color_theme("green")

class Interface:
    def __init__(self, master) -> None:        
        if __arduino__: 
            self.arduino = serial.Serial(arduino_port, baud_rate)
        self.master = master
        self.sensor_readings = []
        self.running = False
        self.time = 0 # em segundos
        self.dir = 0 # 0 -> esquerda, 1 -> direita
    
    def start(self) -> None:
        print("Iniciando experimento...")
        print("Acionando motor...")
        # self.clean_all()
        if(not self.running):
            if(self.time == 0):
                MessageBox.showerror("Erro", "Tempo de Experimento não configurado")
                # CTkMessagebox(title="Erro", message="Tempo de Experimento não configurado", icon="cancel")
                return
            self.running = True
            # Thread para fazer leitura da serial do Arduino
            self.read_thread = Thread(target=self.read_sensor)
            self.read_thread.daemon = True
            self.read_thread.start()
            self.master.after(self.time * 1000, self.stop)
            buttons[0].configure(text="Parar experimento")
        else:
            self.stop()

    def stop(self) -> None:
        self.running = False
        if hasattr(self, 'thread') and self.read_thread.is_alive():
            self.read_thread.join()  # Wait for the thread to finish
        buttons[0].configure(text="Iniciar experimento")
        MessageBox.showinfo("Info", "Teste finalizado")

    def change_dir(self) -> None:
        print("Direção de movimento alterada")
        self.dir = switch.get()

    def set_time(self) -> None:
        dialog = CT.CTkInputDialog(text="Tempo de ensaio:", title="Configurar Tempo de Experimento")
        try:
            self.time = int(dialog.get_input())
            print(f"Tempo de Experimento configurado: {self.time} [s]")
        except Exception as e:
            print(f"[ERROR] {e}")

    def calibrate(self) -> None:
        print("Calibrando algoritmo de visão computacional")

    def focus(self) -> None:
        print("Focando câmera...")
        os.system('v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c auto_exposure=1')
        time.sleep(0.2)
        os.system('v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c focus_automatic_continuous=0')
        time.sleep(0.2)
        os.system('v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c exposure_time_absolute=500')
        time.sleep(0.2)
        os.system('v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c focus_absolute=3')
        time.sleep(0.2)
        os.system('v4l2-ctl -d /dev/v4l/by-id/usb-HP_HP_Webcam_HD-4110-video-index0 -c focus_absolute=4')
    
    def read_sensor(self) -> None:
        # while True:
        for i in range(self.time):
            if(self.running):
                try:
                    value = self.arduino.readline().strip().decode('utf-8')
                    print(f"Luminosidade: {value} [%]")
                    self.sensor_readings.append(float(value))
                    progressbar.set((i + 1) / self.time)
                    # time.sleep(1)
                except Exception as e:
                    print(f"[ERROR] {e}")
                    if(i == 5): self.sensor_readings.append(0.5)
                    else: self.sensor_readings.append(i) # adicionando dado fake, só pra testar o plot
                    progressbar.set((i + 1) / self.time)
                    time.sleep(1)
                    pass
        print("Experimento finalizado")
        
    
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
        self.master.after(thread_delay, self.update_plot)

    def clean_all(self) -> None:
        self.sensor_readings = []
        progressbar.set(0)
        self.ax.clear()

if __name__ == "__main__":
    root = CT.CTk()
    
    # experiment_ctrl = ExperimentControl()

    interface = Interface(root)

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

    progress_var = CT.IntVar()
    progressbar = CT.CTkProgressBar(frame, variable=progress_var, mode='determinate')
    progressbar.grid(row=len(buttons) // 3 + 1, column=2, padx=60, pady=10, sticky="ew")

    root.mainloop()
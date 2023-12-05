import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
from threading import Thread
from tkinter import *
import tkinter.messagebox as MessageBox
import customtkinter as CT
import os
import time
from control.experiment_control import ExperimentControl
from modules.timer import TimerSeconds

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
        self.sensor_readings_x = []
        self.sensor_readings_y = []
        self.running = False
        self.speed = 0 # [1 ~ 255 PWM]
        self.dir = 0 # 0 -> esquerda, 1 -> direita
        self.experiment_ctrl = ExperimentControl()
        self.max_time = 10 # [s]
        self.focus_value = 0 # 0 ~ 10
        self.force = 0.0
        self.distance = 0.0
    
    def start(self) -> None:
        print("[Interface] Iniciando experimento...")
        # self.clean_all()
        if(not self.running):
            self.running = True
            # Thread para fazer leitura dos dados do Arduino
            self.read_thread = Thread(target=self.read_sensor)
            self.read_thread.daemon = True
            self.read_thread.start()
            buttons[0].configure(text="Parar experimento")
        else:
            self.stop()

    def stop(self) -> None:
        self.experiment_ctrl.stop_experiment()
        self.running = False
        buttons[0].configure(text="Iniciar experimento")
        MessageBox.showinfo("Info", "Teste finalizado")

    def calibrate(self) -> None:
        print("[Interface] Calibrando algoritmo de visão computacional")

    def focus(self) -> None:
        print("[Interface] Focando câmera...")
        dialog_focus = CT.CTkInputDialog(text="Foco [0 ~ 10]:", title="Configurar Foco da Câmera")
        try:
            self.focus_value = int(dialog_focus.get_input())
            print(f"[Interface] Foco da câmera configurado: {self.focus_value}")
            self.experiment_ctrl.adjust_focus(self.focus_value)
        except Exception as e:
            print(f"{e}")
            MessageBox.showerror("Erro", e)
    
    def read_sensor(self) -> None:
        self.experiment_ctrl.start_experiment()
        timer = TimerSeconds()
        elapsed_time = timer.elapsed_time()
        while elapsed_time < self.max_time:
            try:
                self.force = self.experiment_ctrl.get_force_reading()
                self.distance = self.experiment_ctrl.get_measured_distance()
                print(self.force, self.distance)
                self.sensor_readings_x.append(float(self.distance))
                self.sensor_readings_y.append(float(self.force))
                progressbar.set(elapsed_time / self.max_time)
            except Exception as exc:
                print(f"{exc}")
            time.sleep(0.07)
            elapsed_time = timer.elapsed_time()
        # self.experiment_ctrl.stop_experiment() # tá dentro de self.stop agora
        self.stop()
        
    def create_plot(self) -> None:
        canvas_frame = CT.CTkFrame(frame)
        canvas_frame.grid(row=len(buttons) // 3 + 1, columnspan=3, pady=10)
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_ylim([y_min, y_max])
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        
    def update_plot(self) -> None:
        self.ax.clear()
        # self.ax.plot(self.sensor_readings, color='green', linewidth=2, marker='o', markersize=5, label='Leitura do Sensor')
        self.ax.plot(self.sensor_readings_x, self.sensor_readings_y, color='green', linewidth=2, marker='o', markersize=5, label='Leitura do Sensor')
        self.ax.set_xlabel('Distância')
        self.ax.set_ylabel('Força')
        self.ax.set_title('Leitura do Sensor em Tempo Real')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.legend(loc='upper right')
        self.canvas.draw()
        self.master.after(thread_delay, self.update_plot)

    def clean_all(self) -> None:
        self.sensor_readings_x = []
        self.sensor_readings_y = []
        progressbar.set(0)
        self.ax.clear()

    def increase(self) -> None:
        self.experiment_ctrl.increase_stress()
    
    def decrease(self) -> None:
        self.experiment_ctrl.decrease_stress()

if __name__ == "__main__":
    #====================== Inicializa interface ==========================#
    root = CT.CTk()
    interface = Interface(root)

    #====================== Tamanho da tela ==========================#
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")

    #====================== Título ==========================#
    root.title("Interface Ensaio de Tração")

    #====================== Frame principal ==========================#
    frame = CT.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill=BOTH, expand=True)

    #====================== Botões principais ==========================#
    button_texts = [
        'Iniciar experimento',
        'Calibrar algoritmo',
        'Focar câmera',
    ]

    button_commands = [
        interface.start,
        interface.calibrate,
        interface.focus
    ]

    buttons = [CT.CTkButton(frame, text=text, width=200, height=60, command=cmd) 
               for text, cmd in zip(button_texts, button_commands)]

    #====================== Posicionamento dos botões principais ==========================#
    for i, button in enumerate(buttons):
        row = i // 3
        col = i % 3
        button.grid(row=row, column=col, padx=20, pady=20)

    for i in range(3):
        frame.columnconfigure(i, weight=1)

    #====================== Comandos do plot ==========================#
    interface.create_plot()
    root.after(thread_delay, interface.update_plot)

    #====================== Frame dos botões + e - ==========================#
    increase_decrease_frame = CT.CTkFrame(frame)
    increase_decrease_frame.grid(row=1, column=0, columnspan=1, pady=10)

    increase_button = CT.CTkButton(increase_decrease_frame, text="+", width=100, height=60, command=interface.increase)
    increase_button.grid(row=0, column=0, padx=5)

    decrease_button = CT.CTkButton(increase_decrease_frame, text="-", width=100, height=60, command=interface.decrease)
    decrease_button.grid(row=0, column=1, padx=5)


    #====================== Limpar ==========================#
    plot_button = CT.CTkButton(frame, text="Limpar", command=interface.clean_all)
    plot_button.grid(row=len(buttons) // 3, column=1, pady=10)

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(len(buttons) // 3 + 1, weight=1)

    #====================== Progress Bar ==========================#
    progress_var = CT.IntVar()
    progressbar = CT.CTkProgressBar(frame, variable=progress_var, mode='determinate')
    progressbar.grid(row=len(buttons) // 3, column=2, padx=60, pady=10, sticky="ew")

    root.mainloop()
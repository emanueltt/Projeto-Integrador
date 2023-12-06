import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
from tkinter import *
import tkinter.messagebox as MessageBox
import customtkinter as CT
import time
from control.experiment_control import ExperimentControl
from modules.timer import TimerSeconds

# Constantes
arduino_port = '/dev/ttyACM0'
baud_rate = 9600
thread_delay = 500 # ms
CT.set_appearance_mode("dark")
CT.set_default_color_theme("green")

class Interface:
    def __init__(self, master) -> None:        
        self.master = master
        self.sensor_readings_x = []
        self.sensor_readings_y = []
        self.running = False
        self.experiment_ctrl = ExperimentControl()
        self.max_time = 15 # [s]
        self.focus_value = 0 # 0 ~ 10
        self.force = 0.0
        self.distance = 0.0
        self.read_thread = None
    
    def start(self) -> None:
        print("[Interface] Iniciando experimento...")
        self.clean_all()
        if(not self.running):
            print("[Interface] Iniciando experimento...")
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
        print("Teste finalizado")
        MessageBox.showinfo("Info", "Teste finalizado")

    def set_time(self) -> None:
        print("[Interface] Configurando tempo de experimento")
        dialog_set_time = CT.CTkInputDialog(text="Tempo [s]:", title="Configurar tempo de experimento")
        try:
            self.max_time = int(dialog_set_time.get_input())
            print(f"[Interface] Tempo configurado: {self.max_time} [s]")
        except Exception as e:
            print(f"{e}")
            MessageBox.showerror("Erro", e)

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
        last_addition = 0
        while elapsed_time < self.max_time and self.running:
            try:
                self.force = self.experiment_ctrl.get_force_reading()
                self.distance = self.experiment_ctrl.get_measured_distance()
                cv2.imshow("imagem", self.experiment_ctrl._vision_control._image_queue.get())
                cv2.waitKey(1)
                print(self.force, self.distance)
                if self.force is None or self.distance is None:
                    continue
                elif float(self.distance) < last_addition:
                    continue
                last_addition = float(self.distance)
                self.sensor_readings_x.append(float(self.distance))
                self.sensor_readings_y.append(float(self.force))
                progressbar.set(elapsed_time / self.max_time)
            except Exception as exc:
                print(f"{exc}")
            time.sleep(0.07)
            elapsed_time = timer.elapsed_time()
            print(elapsed_time)
        progressbar.set(1)
        cv2.destroyAllWindows()
        # self.experiment_ctrl.stop_experiment() # tá dentro de self.stop agora
        self.stop()
        
    def create_plot(self) -> None:
        canvas_frame = CT.CTkFrame(frame)
        canvas_frame.grid(row=len(buttons) // 3 + 1, columnspan=3, pady=10)
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        
    def update_plot(self) -> None:
        self.ax.clear()
        self.ax.plot(self.sensor_readings_x, self.sensor_readings_y, color='green', linewidth=2, marker='o', markersize=5, label='Leitura do Sensor')
        self.ax.set_xlabel('Distância (mm)')
        self.ax.set_ylabel('Força (mN)')
        self.ax.set_title('Leitura do Sensor em Tempo Real')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.legend(loc='upper right')
        self.canvas.draw()
        self.master.after(thread_delay, self.update_plot)

    def clean_all(self) -> None:
        print("[Interface] clean all")
        self.sensor_readings_x = []
        self.sensor_readings_y = []
        progressbar.set(0)
        self.ax.clear()
        # if(self.read_thread.is_alive()): self.read_thread.join()

    def increase(self) -> None:
        print("[Interface] Increase")
        self.experiment_ctrl.increase_stress()
    
    def decrease(self) -> None:
        print("[Interface] Decrease")
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
        'Configurar tempo do experimento',
        'Focar câmera',
    ]

    button_commands = [
        interface.start,
        interface.set_time,
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
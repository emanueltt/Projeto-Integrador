import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
from threading import Thread
from tkinter import *
import customtkinter

# Defines
arduino_port = '/dev/ttyACM0'
baud_rate = 9600
thread_delay = 500 # ms
y_min = 0
y_max = 100 # [%]
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

arduino = serial.Serial(arduino_port, baud_rate)
sensor_readings = []

def change_brightness():
    brightness = slider.get()
    print("brightness: ", brightness)
    arduino.write(bytes(str(brightness) + '\n', 'utf-8'))

def slider_handler(value):
    print(value)

def read_sensor():
    global sensor_readings
    while True:
        print("Reading sensor values")
        try:
            value = arduino.readline().strip().decode('utf-8')
            print("value: ", value)
            sensor_readings.append(value)
        except ValueError:
            print("ValueError")
            pass

def update_plot():
    global y_min, y_max
    ax.clear()
    ax.plot(sensor_readings, color='green', linewidth=2, marker='o', markersize=5, label='Leitura do Sensor')
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Sensor')
    ax.set_title('Leitura do Sensor em Tempo Real')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper right')
    canvas.draw()
    root.after(thread_delay, update_plot)

if __name__ == "__main__":
    # Thread para fazer leitura da serial do Arduino
    read_thread = Thread(target=read_sensor)
    read_thread.daemon = True
    read_thread.start()

    root = customtkinter.CTk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.geometry(f"{screen_width}x{screen_height}")
    root.title("Interface Ensaio de Tração")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill=BOTH, expand=True)

    label = customtkinter.CTkLabel(master=frame, text="Controle a luminosidade do LED", justify=customtkinter.LEFT)
    label.pack(pady=10, padx=10)

    slider = customtkinter.CTkSlider(master=frame, command=slider_handler, from_=0, to=255, number_of_steps=255)
    slider.pack(pady=10, padx=10)
    slider.set(0.5)

    button = customtkinter.CTkButton(master=frame, text='Enviar para o Arduino', command=change_brightness)
    button.pack(pady=10, padx=10)

    fig, ax = plt.subplots(figsize=(4, 8))
    ax.set_ylim([y_min, y_max])
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    root.after(thread_delay, update_plot)

    root.mainloop()
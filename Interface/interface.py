import serial
from tkinter import *
import customtkinter

arduino_port = '/dev/ttyACM0'
baud_rate = 9600

def change_brightness():
    brightness = slider.get()
    print("brightness: ", brightness)
    arduino.write(bytes(str(brightness) + '\n', 'utf-8'))

def slider_handler(value):
    print(value)

if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("green")

    root = customtkinter.CTk()

    root.geometry('500x250')
    root.title("Interface Ensaio de Tração")

    label = customtkinter.CTkLabel(master=root, text="Controle a luminosidade do LED")
    label.place(relx=0.5, rely=0.25, anchor=CENTER)

    slider = customtkinter.CTkSlider(master=root, from_=0, to=255, number_of_steps=255, command=slider_handler)
    slider.place(relx=0.5, rely=0.45, anchor=CENTER)

    button = customtkinter.CTkButton(master=root, text='Enviar para o Arduino', command=change_brightness)
    button.place(relx=0.5, rely=0.65, anchor=CENTER)

    arduino = serial.Serial(arduino_port, baud_rate)

    root.mainloop()
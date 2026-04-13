import tkinter as tk
from tkinter import ttk
from typing import Callable
from pathlib import Path

from . import consts as const


class MenuView:
    def __init__(self, master: tk.Widget, on_start: Callable[[], None]) -> None:
        self.master = master
        self.frame = tk.Frame(master, width=300, height=220)
        self.frame.grid(row=0, column=0)
        self.selected_texture = None
        
        base_dir = Path(__file__).resolve().parent.parent
        textures_dir = base_dir.joinpath('textures')
        
        self.title_label = tk.Label(
            self.frame,
            text=const.GAME_TITLE,
            font=("Arial", 16),
        )
        self.title_label.grid(row=0, column=0, padx=12, pady=(16, 10))

        self.start_button = tk.Button(
            self.frame,
            text="Start Game",
            command=on_start,
            activebackground="blue",
            width=16,
        )
        self.start_button.grid(row=2, column=0, padx=12, pady=(8, 16))

        self.status_label = tk.Label(self.frame, text="", wraplength=260)
        self.status_label.grid(row=1, column=0, padx=12, pady=(8, 50))

        self.exit_button = tk.Button(
            self.frame,
            text="Exit",
            command=self.close_game,
            activebackground="red",
            width=16,
        )
        self.exit_button.grid(row=3, column=0, padx=12, pady=(8, 16))

        self.choice_of_texture_button = tk.Button(
            self.frame,
            text="Change background",
            command= self.open_second_window,
            width=20,
        )
        self.choice_of_texture_button.grid(row=4, column=0,padx=12, pady=(8, 16))

    
        self.selected_car = "car_1.png"
        self.car_img = tk.PhotoImage(file=textures_dir.joinpath(self.selected_car))
        self.car_img = self.car_img.zoom(3, 3)
        self.car_img_label = tk.Label(self.frame, image=self.car_img)
        self.car_img_label.grid(row=6, column=0, padx=12, pady=(8, 8))
        
        self.choice_of_car_combobox = ttk.Combobox(
            self.frame,
            values = ["car_1.png", "car_2.png", "car_3.png", "car_4.png"],
            state = "readonly",
            width=16,
        )
        self.choice_of_car_combobox.grid(row=5, column=0,padx=12, pady=(8, 16))
        self.choice_of_car_combobox.set(self.selected_car)
        self.choice_of_car_combobox.bind("<<ComboboxSelected>>", self.change_car_img)
        
    def change_car_img(self, event=None) -> None:
        base_dir = Path(__file__).resolve().parent.parent
        textures_dir = base_dir.joinpath('textures')
        
        self.selected_car = self.choice_of_car_combobox.get()
        self.car_img = tk.PhotoImage(file=textures_dir.joinpath(self.selected_car))
        self.car_img = self.car_img.zoom(3, 3)
        self.car_img_label.configure(image=self.car_img)
        self.set_status(f"Selected car: {self.selected_car}")
        
    def show(self) -> None:
        self.frame.grid()
        
    def close_game(self) -> None:
        self.master.winfo_toplevel().destroy()

    def hide(self) -> None:
        self.frame.grid_remove()

    def set_status(self, message: str) -> None:
        self.status_label.configure(text=message)
        
    def open_second_window(self) -> None:
        self.second_window = SecondWindow(self.master, self)
        
    def set_texture(self,texture_file:str) -> None:
        self.selected_texture = texture_file
        #self.start_button.configure(state="normal")
        self.set_status(f"Selected texture: {texture_file}")

class SecondWindow:
    def __init__(self, master:tk.Widget, menu) -> None:
        self.menu = menu
        self.window = tk.Toplevel(master)
        self.window.title("Choose texture")
        self.frame = tk.Frame(self.window)
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        #path to the photos
        base_dir = Path(__file__).resolve().parent.parent
        textures_dir = base_dir.joinpath('textures')
        
        self.title_label = tk.Label(
            self.frame,
            text="Choose the texture",
            anchor='center',
            font=("Arial", 16),
        )
        self.title_label.grid(row=0, column=1, columnspan=2, padx=12, pady=(16, 10))

        self.button2 = tk.Button(
            self.frame,
            text="Road",
            width=10,
            command= lambda: self.choose_texture("road_2.png"),
        )
        self.button2.grid(row=1, column=1, padx=4, pady=(4, 4))

        self.img2 = tk.PhotoImage(file=textures_dir.joinpath('road_2.png'))
        self.img2 = self.img2.zoom(3, 3)
        self.img2_label = tk.Label(self.frame, image=self.img2)
        self.img2_label.grid(row=2, column=1, padx=4, pady=(4,4))
        
        self.button3 = tk.Button(
            self.frame,
            text="Sand",
            width=10,
            command= lambda: self.choose_texture("sand_1.png"),
        )
        self.button3.grid(row=1, column=2, padx=4, pady=(4, 4))
        
        self.img3 = tk.PhotoImage(file= textures_dir.joinpath('sand_1.png'))
        self.img3 = self.img3.zoom(3, 3)
        self.img3_label = tk.Label(self.frame, image=self.img3)
        self.img3_label.grid(row=2, column=2, padx=4, pady=(4,4))
        
        self.button5 = tk.Button(
            self.frame,
            text="Grass 2",
            width=10,
            command= lambda: self.choose_texture("grass_2.png"),
        )
        self.button5.grid(row=3, column=1, padx=4, pady=(4, 4))
        
        self.img5 = tk.PhotoImage(file= textures_dir.joinpath('grass_2.png'))
        self.img5 = self.img5.zoom(3, 3)
        self.img5_label = tk.Label(self.frame, image=self.img5)
        self.img5_label.grid(row=4, column=1, padx=4, pady=(4,4))

        self.button6 = tk.Button(
            self.frame,
            text="Flowers",
            width=10,
            command= lambda: self.choose_texture("grass_3.png"),
        )
        self.button6.grid(row=3, column=2, padx=4, pady=(4, 4))
        
        self.img6 = tk.PhotoImage(file= textures_dir.joinpath('grass_3.png'))
        self.img6 = self.img6.zoom(3, 3)
        self.img6_label = tk.Label(self.frame, image=self.img6)
        self.img6_label.grid(row=4, column=2, padx=4, pady=(4,4))
        
        self.button7 = tk.Button(
            self.frame,
            text="Grass 1",
            width=10,
            command= lambda: self.choose_texture("grass_1.png"),
        )
        self.button7.grid(row=5, column=1, columnspan=2, padx=4, pady=(4, 4))
        
        self.img7 = tk.PhotoImage(file= textures_dir.joinpath('grass_1.png'))
        self.img7 = self.img7.zoom(3, 3)
        self.img7_label = tk.Label(self.frame, image=self.img7)
        self.img7_label.grid(row=6, column=1, columnspan=2, padx=4, pady=(4,4))
        
        self.window.update_idletasks()
        self.window.minsize(self.window.winfo_width(), self.window.winfo_height())

        
    def show(self) -> None:
        self.window.grid()

    def hide(self) -> None:
        self.window.grid_remove()

    def choose_texture(self, texture_file: str) -> None:
        self.menu.set_texture(texture_file)
        self.window.destroy()
        
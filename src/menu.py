import tkinter as tk
from typing import Callable
from pathlib import Path

from . import consts as const


class MenuView:
    def __init__(self, master: tk.Widget, on_start: Callable[[], None]) -> None:
        self.master = master
        self.frame = tk.Frame(master, width=300, height=220)
        self.frame.grid(row=0, column=0)
        self.selected_texture = None

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
        self.start_button.grid(row=1, column=0, padx=12, pady=(8, 8))

        self.status_label = tk.Label(self.frame, text="", wraplength=260)
        self.status_label.grid(row=2, column=0, padx=12, pady=(8, 12))

        self.choice_of_texture_button = tk.Button(
            self.frame,
            text="Change texture",
            command= self.open_second_window,
            width=20,
        )
        self.choice_of_texture_button.grid(row=3, column=0,padx=12, pady=(8, 16))
    
        self.choice_of_car_button = tk.Button(
            self.frame,
            text="Change car",
            width=16,
        )
        self.choice_of_car_button.grid(row=4, column=0,padx=12, pady=(8, 16))
    
    def show(self) -> None:
        self.frame.grid()

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
        self.window.geometry("400x200")
        self.frame = tk.Frame(self.window)
        self.frame.grid(row=0, column=0)

        #path to the photos
        base_dir = Path(__file__).resolve().parent.parent
        textures_dir = base_dir.joinpath('textures')
        
        self.title_label = tk.Label(
            self.frame,
            text="Choose the texture",
            anchor='center',
            font=("Arial", 16),
        )
        self.title_label.grid(row=0, column=1, padx=12, pady=(16, 10))

        self.button1 = tk.Button(
            self.frame,
            text="Road 1",
            width=10,
            command= lambda: self.choose_texture("road_1.png"),
        )
        self.button1.grid(row=1, column=0, padx=4, pady=(4,4))
        
        self.img1 = tk.PhotoImage(file= textures_dir.joinpath('road_1.png'))
        self.img1_label = tk.Label(self.frame, image=self.img1)
        self.img1_label.grid(row=2, column=0, padx=4, pady=(4,4))

        self.button2 = tk.Button(
            self.frame,
            text="Road 2",
            width=10,
            command= lambda: self.choose_texture("road_2.png"),
        )
        self.button2.grid(row=1, column=1, padx=4, pady=(4, 4))

        self.img2 = tk.PhotoImage(file=textures_dir.joinpath('road_2.png'))
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
        self.img3_label = tk.Label(self.frame, image=self.img3)
        self.img3_label.grid(row=2, column=2, padx=4, pady=(4,4))


        self.button4 = tk.Button(
            self.frame,
            text="Grass 1",
            width=10,
            command= lambda: self.choose_texture("grass_1.png"),
        )
        self.button4.grid(row=3, column=0, padx=4, pady=(4, 4))
        
        self.img4 = tk.PhotoImage(file= textures_dir.joinpath('grass_1.png'))
        self.img4_label = tk.Label(self.frame, image=self.img4)
        self.img4_label.grid(row=4, column=0, padx=4, pady=(4,4))

        
        self.button5 = tk.Button(
            self.frame,
            text="Grass 2",
            width=10,
            command= lambda: self.choose_texture("grass_2.png"),
        )
        self.button5.grid(row=3, column=1, padx=4, pady=(4, 4))
        
        self.img5 = tk.PhotoImage(file= textures_dir.joinpath('grass_2.png'))
        self.img5_label = tk.Label(self.frame, image=self.img5)
        self.img5_label.grid(row=4, column=1, padx=4, pady=(4,4))

        self.button6 = tk.Button(
            self.frame,
            text="Grass 3",
            width=10,
            command= lambda: self.choose_texture("grass_3.png"),
        )
        self.button6.grid(row=3, column=2, padx=4, pady=(4, 4))
        
        self.img6 = tk.PhotoImage(file= textures_dir.joinpath('grass_3.png'))
        self.img6_label = tk.Label(self.frame, image=self.img6)
        self.img6_label.grid(row=4, column=2, padx=4, pady=(4,4))

        
    def show(self) -> None:
        self.window.grid()

    def hide(self) -> None:
        self.window.grid_remove()

    def choose_texture(self, texture_file: str) -> None:
        self.menu = self.menu
        self.menu.set_texture(texture_file)
        self.window.destroy()
        
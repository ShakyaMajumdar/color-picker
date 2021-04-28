import tkinter as tk
import pyautogui
import PIL.ImageGrab
from PIL import Image
from time import sleep

class Overlay:
    def __init__(self,parent):
        self.parent = parent

        self.root = tk.Tk()

        self.active = False

        self.root.overrideredirect(True)
        self.root.wait_visibility(self.root)
        self.root.configure(background='black')
        self.root.wm_attributes('-alpha',0.002)
        #self.root.geometry("500x500+1+1")
        self.root.attributes('-topmost', True)
        self.root.bind('<Button-1>', self.get_px)
        self.root.config(cursor="crosshair")
        self.root.withdraw()

    def get_px(self,event):
        x,y=pyautogui.position()
        
        #self.root.attributes('-alpha',0.0)
        self.root.withdraw()
        print('getting col')
        px = PIL.ImageGrab.grab(bbox=(x,y,x+1,y+1), include_layered_windows=False, all_screens=True)
        print('got col')
        #self.root.attributes('-alpha',0.002)
        color_rgb = (px.load()[0,0])
        color_hex = '#%02x%02x%02x' % (color_rgb)
        print(color_rgb,color_hex,x,y)
        self.parent.selected_color.create_rectangle(0,0,25,25,fill=f'{color_hex}')
        self.active = False

    def update(self):
        x,y=pyautogui.position()
        self.root.geometry(f'600x600+{x-300}+{y-300}')
        if not self.active:
            print('overlay deactivated')
        else:
            self.root.after(1,self.update)

    def start(self):
        self.root.deiconify()
        self.active = True
        self.root.after(1,self.update)

class Main:
    def __init__(self):
        self.root = tk.Tk()

        self.overlay = Overlay(self.root)

        self.root.geometry("250x350+1+1")

        self.root.button_eye_drop = tk.Button(self.root, text = 'Eye Drop', width = 25)
        self.root.button_eye_drop['command'] = lambda arg1 = self.root : self.overlay.start()
        self.root.button_eye_drop.pack()

        self.root.selected_color = tk.Canvas(self.root,width=25,height=25)
        self.root.selected_color.create_rectangle(0,0,25,25,fill='gray')
        self.root.selected_color.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        self.overlay.active = False
        self.overlay.root.destroy()
        self.root.destroy()

def main():
    main = Main()

if __name__ == '__main__':
    main()

import tkinter as tk
import win32gui
import win32con
import math
import time

root = tk.Tk()
root.overrideredirect(True)  # Kein Fensterrahmen
root.attributes("-topmost", True)  # Immer im Vordergrund
root.attributes("-transparentcolor", "black")  # Schwarz wird unsichtbar
root.config(bg="black")

size = 120
canvas = tk.Canvas(root, width=size, height=size, bg="black", highlightthickness=0)
canvas.pack()

# Fenster klickdurchlässig machen, damit du normal arbeiten kannst
hwnd = win32gui.FindWindow(None, root.title())
styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)

# Startposition
curr_x, curr_y = 500.0, 500.0
start_time = time.time()

def update():
    global curr_x, curr_y
    t = time.time() - start_time

    # Mausposition abfragen + leichtes Offset oben links vom Cursor
    mouse_x = root.winfo_pointerx() - 45
    mouse_y = root.winfo_pointery() - 45

    # Sanfte Verfolgung (Lerp)
    curr_x += (mouse_x - curr_x) * 0.08
    curr_y += (mouse_y - curr_y) * 0.08

    # Schwebebewegung (Sinuswelle)
    hover_y = math.sin(t * 4) * 6
    root.geometry(f"{size}x{size}+{int(curr_x - size/2)}+{int(curr_y - size/2 + hover_y)}")

    # Navi zeichnen (Flügel + leuchtender Kern)
    canvas.delete("all")
    cx, cy = size // 2, size // 2
    flap = math.sin(t * 18) * 8  # Flügelschlag-Geschwindigkeit

    # Obere Flügel
    canvas.create_oval(cx - 28, cy - 22 + flap, cx - 2, cy - 2, fill="#d9f7ff", outline="#70e1ff")
    canvas.create_oval(cx + 2, cy - 22 + flap, cx + 28, cy - 2, fill="#d9f7ff", outline="#70e1ff")
    # Untere Flügel
    canvas.create_oval(cx - 20, cy + 2, cx - 2, cy + 16 - flap*0.5, fill="#b8f0ff", outline="#70e1ff")
    canvas.create_oval(cx + 2, cy + 2, cx + 20, cy + 16 - flap*0.5, fill="#b8f0ff", outline="#70e1ff")

    # Äußerer Schein & innerer Kern
    canvas.create_oval(cx - 14, cy - 14, cx + 14, cy + 14, fill="#00bfff", outline="")
    canvas.create_oval(cx - 8, cy - 8, cx + 8, cy + 8, fill="#ffffff", outline="")

    root.after(16, update)  # ~60 FPS

update()
root.mainloop()
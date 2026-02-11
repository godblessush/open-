import tkinter as tk
import math

# Window setup
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)

size = 400
root.geometry(f"{size}x{size}+800+200")

root.config(bg="black")
root.wm_attributes("-transparentcolor", "black")

canvas = tk.Canvas(root, width=size, height=size, bg="black", highlightthickness=0)
canvas.pack()

center = size // 2
radius = 150

# Main outer ring
outer_ring = canvas.create_oval(
    center - radius,
    center - radius,
    center + radius,
    center + radius,
    outline="#00f2ff",
    width=3
)

# Inner ring
inner_ring = canvas.create_oval(
    center - 90,
    center - 90,
    center + 90,
    center + 90,
    outline="#00f2ff",
    width=2
)

# Core
core = canvas.create_oval(
    center - 40,
    center - 40,
    center + 40,
    center + 40,
    fill="#00f2ff",
    outline=""
)

# Center text
text = canvas.create_text(
    center, center,
    text="JARVIS",
    fill="black",
    font=("Consolas", 14, "bold")
)

angle = 0
pulse = 0
pulse_dir = 1

def draw_rotating_arc():
    global angle
    canvas.delete("arc")

    start = angle
    extent = 40

    canvas.create_arc(
        center - radius,
        center - radius,
        center + radius,
        center + radius,
        start=start,
        extent=extent,
        style="arc",
        outline="#00ffff",
        width=6,
        tags="arc"
    )

    angle += 4
    root.after(30, draw_rotating_arc)

def pulse_core():
    global pulse, pulse_dir

    pulse += pulse_dir * 2
    if pulse > 30:
        pulse_dir = -1
    elif pulse < 0:
        pulse_dir = 1

    brightness = 180 + pulse
    color = f'#{0:02x}{brightness:02x}{255:02x}'
    canvas.itemconfig(core, fill=color)

    root.after(50, pulse_core)

# Dragging
def start_move(event):
    root.x = event.x
    root.y = event.y

def move_window(event):
    x = event.x_root - root.x
    y = event.y_root - root.y
    root.geometry(f"+{x}+{y}")

canvas.bind("<Button-1>", start_move)
canvas.bind("<B1-Motion>", move_window)

# Close on ESC
root.bind("<Escape>", lambda e: root.destroy())

draw_rotating_arc()
pulse_core()
root.mainloop()

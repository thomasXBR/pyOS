import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

def show_main_ui():
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # ===== Helper Functions =====
    def get_current_time():
        return datetime.now().strftime("%H:%M:%S")

    def load_bg_image(index):
        try:
            img = Image.open(bg_image_paths[index])
            img = img.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Failed to load image {bg_image_paths[index]}: {e}")
            return None

    def cycle_background_image():
        current_image_index[0] = (current_image_index[0] + 1) % len(bg_image_paths)
        new_img = load_bg_image(current_image_index[0])
        if new_img:
            bg_label.configure(image=new_img)
            bg_label.image = new_img

    def update_clock():
        time_label.config(text=get_current_time())
        root.after(1000, update_clock)

    def clear_canvas():
        draw_canvas.delete("all")

    def start_draw(event):
        last_x[0], last_y[0] = event.x, event.y

    def draw(event):
        if last_x[0] is not None and last_y[0] is not None:
            draw_canvas.create_line(last_x[0], last_y[0], event.x, event.y, fill="black", width=2)
            last_x[0], last_y[0] = event.x, event.y

    def stop_draw(event):
        last_x[0], last_y[0] = None, None

    def hide_all_frames():
        start_frame.place_forget()
        settings_frame.place_forget()
        draw_frame.place_forget()
        is_start_visible.set(False)
        is_settings_visible.set(False)
        is_draw_visible.set(False)

    def show_above_button(frame, button_widget, visible_flag):
        if visible_flag.get():
            frame.place_forget()
            visible_flag.set(False)
        else:
            hide_all_frames()
            x = button_widget.winfo_rootx() - root.winfo_rootx()
            y = button_widget.winfo_rooty() - root.winfo_rooty() - frame.winfo_reqheight() - 10
            frame.place(x=x, y=y)
            visible_flag.set(True)

    def show_centered_draw():
        if is_draw_visible.get():
            draw_frame.place_forget()
            is_draw_visible.set(False)
        else:
            hide_all_frames()
            draw_frame.place(relx=0.5, rely=0.5, anchor="center")
            is_draw_visible.set(True)

    def quit_app():
        root.destroy()

    def show_about():
        tk.messagebox.showinfo("About PyOS", "PyOS version 1.1.1\nCreated by: xbr")

    def toggle_dark_mode():
        nonlocal is_dark_mode
        is_dark_mode = not is_dark_mode
        new_color = "#003b4c" if is_dark_mode else "white"

        bottom_frame.config(bg=new_color)
        time_label.config(bg=new_color, fg="white" if is_dark_mode else "black")

        for frame in [start_frame, settings_frame, draw_frame, draw_content]:
            frame.config(bg=new_color)

        clear_btn.config(bg="lightgrey" if not is_dark_mode else "#006778")
        draw_canvas.config(bg="white" if not is_dark_mode else "#b0e0e6")

    # ===== Background Setup =====
    bg_image_paths = [
        "assets/pyOS_wallpaper1.jpg",
        "assets/pyOS_wallpaper2.jpg",
        "assets/pyOS_wallpaper3.jpg",
        "assets/coplandos_wallpaper.jpg",
        "assets/lain_wallpaper.jpg",
        "assets/windows7.jpg"
    ]
    current_image_index = [0]

    root.update_idletasks()
    bg_img_obj = load_bg_image(current_image_index[0])
    bg_label = tk.Label(root, image=bg_img_obj)
    bg_label.image = bg_img_obj
    bg_label.place(relwidth=1, relheight=1)

    root.configure(background="black")

    # ===== Bottom Frame (Control Bar) =====
    bottom_frame = tk.Frame(root, bg="white")
    bottom_frame.pack(side='bottom', fill='x')

    time_label = tk.Label(bottom_frame, text=get_current_time(), bg="white", fg="black", font=("Courier", 12))
    time_label.pack(side='left', padx=10)

    update_clock()

    # ===== Frames =====
    start_frame = tk.Frame(root, bg="white", bd=2, relief='ridge')
    settings_frame = tk.Frame(root, bg="white", bd=2, relief='ridge')
    draw_frame = tk.Frame(root, bg="white", bd=2, relief='ridge', width=533, height=400)
    draw_frame.pack_propagate(False)

    draw_content = tk.Frame(draw_frame, bg="white")
    draw_content.pack(expand=True, fill="both", padx=10, pady=10)

    clear_btn = tk.Button(draw_content, text="Clear", command=clear_canvas, bg="lightgrey")
    clear_btn.pack(pady=(0, 5))

    draw_canvas = tk.Canvas(draw_content, bg="white")
    draw_canvas.pack(expand=True, fill="both")

    draw_canvas.bind("<Button-1>", start_draw)
    draw_canvas.bind("<B1-Motion>", draw)
    draw_canvas.bind("<ButtonRelease-1>", stop_draw)

    last_x, last_y = [None], [None]

    # ===== Frame Visibility Flags =====
    is_start_visible = tk.BooleanVar(value=False)
    is_settings_visible = tk.BooleanVar(value=False)
    is_draw_visible = tk.BooleanVar(value=False)
    is_dark_mode = False

    # ===== Frame Contents =====
    tk.Button(start_frame, text="Exit", command=quit_app).pack(padx=20, pady=10)
    tk.Button(settings_frame, text="Change background", command=cycle_background_image).pack(padx=20, pady=10)
    tk.Button(settings_frame, text="Dark mode", command=toggle_dark_mode).pack(padx=20, pady=10)

    # ===== Control Buttons =====
    start_btn = tk.Button(bottom_frame, text="START")
    settings_btn = tk.Button(bottom_frame, text="SETTINGS")
    draw_btn = tk.Button(bottom_frame, text="DRAW", command=show_centered_draw)
    about_btn = tk.Button(bottom_frame, text="ABOUT", command=show_about)

    start_btn.pack(side='left', padx=(10, 5), pady=10)
    settings_btn.pack(side='left', padx=(10, 5), pady=10)
    draw_btn.pack(side='left', padx=(10, 5), pady=10)
    about_btn.pack(side='left', padx=(10, 5), pady=10)

    start_btn.config(command=lambda: show_above_button(start_frame, start_btn, is_start_visible))
    settings_btn.config(command=lambda: show_above_button(settings_frame, settings_btn, is_settings_visible))


# ===== Main App Entry Point =====
root = tk.Tk()
root.title("PyOS")
root.state("zoomed")  # Fullscreen
root.configure(background="black")

# ===== Boot Screen with Background Image =====
boot_img = Image.open("assets/lain_wallpaper.jpg")
boot_img = boot_img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
boot_bg = ImageTk.PhotoImage(boot_img)

boot_label = tk.Label(root, image=boot_bg)
boot_label.image = boot_bg
boot_label.place(relwidth=1, relheight=1)

tk.Label(
    root.attributes(fullscreen=True),
    text="Booting PyOS...",
    fg="lime",
    bg="black",
    font=("Courier", 18)
).place(relx=0.5, rely=0.5, anchor="center")

# Show main UI after 3 seconds
root.after(3000, show_main_ui)
root.mainloop()

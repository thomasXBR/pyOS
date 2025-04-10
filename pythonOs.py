import tkinter as tk

def show_main_ui():
    # Clear the opening screen
    for widget in root.winfo_children():
        widget.destroy()
    
    # Now build your main UI here
    root.configure(background="bisque")

    tk.Label(root, text="Welcome to PyOS", bg="bisque", font=("Arial", 16)).pack(pady=20)
    tk.Label(root, text="Created by: xbr", bg="bisque").pack()

    bottom_frame = tk.Frame(root, bg="white")
    bottom_frame.pack(side='bottom', fill='x')

    # Frame and toggle setup (like before)
    options_frame = tk.Frame(root, bg="white", bd=2, relief='ridge')

    def toggle_options():
        if options_frame.winfo_ismapped():
            options_frame.pack_forget()
        else:
            options_frame.pack(side='bottom', pady=(0, 5))

    def quit_app():
        root.destroy()

    # Exit button inside options frame
    tk.Button(options_frame, text="Exit", command=quit_app).pack(padx=10, pady=5)

    # START button
    tk.Button(bottom_frame, text="START", command=toggle_options).pack(side='left', padx=(10, 5), pady=10)

# -------------------- MAIN APP START -------------------- #
root = tk.Tk()
root.title("PyOS")
root.geometry("800x500+50+50")
root.configure(background="black")
root.minsize(800, 500)
root.maxsize(800, 500)

# Simulated boot screen
tk.Label(root, text="Booting PyOS...", fg="lime", bg="black", font=("Courier", 18)).pack(expand=True)

# After 3 seconds, switch to main UI
root.after(3000, show_main_ui)

root.mainloop()

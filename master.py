import tkinter as tk


def main():
    root = tk.Tk()

    root.title("Library Management System")
    root.geometry("900x600")
    root.minsize(800, 500)

    title_label = tk.Label(
        root,
        text="Library Management System",
        font=("Arial", 24, "bold")
    )
    title_label.pack(pady=50)

    status_label = tk.Label(
        root,
        text="Project setup completed successfully!",
        font=("Arial", 14)
    )
    status_label.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
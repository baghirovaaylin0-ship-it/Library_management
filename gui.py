import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from file_manager import load_books
from file_manager import load_members
from file_manager import save_books
from file_manager import save_members
from library import Library
from models import Book
from models import Member
from validators import validate_book_id
from validators import validate_member_id
from validators import validate_name
from validators import validate_phone
from validators import validate_email
from validators import validate_year
from validators import validate_category

library = Library()
library.books = load_books()
library.members = load_members()

window = tk.Tk()
window.title("Library Management System")
window.geometry("950x620")

status_text = tk.StringVar()
status_text.set("Program hazirdir")

def set_status(text):
    status_text.set(text)

def clear_entries(entries):
    for entry in entries:
        entry.delete(0, tk.END)

def find_book(book_id):
    return library.find_book(book_id)

def find_member(member_id):
    return library.find_member(member_id)

def save_all():
    try:
        save_books(library.books)
        save_members(library.members)
        return True
    except Exception as error:
        messagebox.showerror("Save error", str(error))
        return False

def selected_book_id():
    selected = book_tree.selection()

    if len(selected) == 0:
        return None

    values = book_tree.item(selected[0], "values")
    return values[0]

def selected_member_id():
    selected = member_tree.selection()

    if len(selected) == 0:
        return None

    values = member_tree.item(selected[0], "values")
    return values[0]

def refresh_books(book_list=None):
    for row in book_tree.get_children():
        book_tree.delete(row)

    if book_list is None:
        book_list = library.books

    for book in book_list:
        if book.available:
            available_text = "Yes"
        else:
            available_text = "No"

        values = (
            book.book_id,
            book.title,
            book.author,
            book.year,
            book.category,
            available_text
        )
        book_tree.insert("", "end", values=values)

    set_status(str(len(book_list)) + " book shown")

def refresh_members(member_list=None):
    for row in member_tree.get_children():
        member_tree.delete(row)

    if member_list is None:
        member_list = library.members

    for member in member_list:
        borrowed_text = ""

        for book_id in member.borrowed_books:
            if borrowed_text != "":
                borrowed_text = borrowed_text + ", "

            borrowed_text = borrowed_text + str(book_id)

        if borrowed_text == "":
            borrowed_text = "-"

        values = (
            member.member_id,
            member.name,
            member.phone,
            member.email,
            borrowed_text
        )
        member_tree.insert("", "end", values=values)

    set_status(str(len(member_list)) + " member shown")

def fill_book_form(event=None):
    book_id = selected_book_id()

    if book_id is None:
        return

    book = find_book(book_id)

    if book is None:
        return

    clear_entries(book_entries)
    book_id_entry.insert(0, book.book_id)
    title_entry.insert(0, book.title)
    author_entry.insert(0, book.author)
    year_entry.insert(0, book.year)
    category_entry.insert(0, book.category)

def fill_member_form(event=None):
    member_id = selected_member_id()

    if member_id is None:
        return

    member = find_member(member_id)

    if member is None:
        return

    clear_entries(member_entries)
    member_id_entry.insert(0, member.member_id)
    name_entry.insert(0, member.name)
    phone_entry.insert(0, member.phone)
    email_entry.insert(0, member.email)

def get_book_form_data():
    book_id = book_id_entry.get().strip()
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    year = year_entry.get().strip()
    category = category_entry.get().strip()

    return book_id, title, author, year, category

def validate_book_form(book_id, title, author, year, category):
    if not validate_book_id(book_id):
        messagebox.showwarning("Warning", "Book ID is wrong")
        return False

    if title == "":
        messagebox.showwarning("Warning", "Title is empty")
        return False

    if not validate_name(author):
        messagebox.showwarning("Warning", "Author name is wrong")
        return False

    if not validate_year(year):
        messagebox.showwarning("Warning", "Year is wrong")
        return False

    if not validate_category(category):
        messagebox.showwarning("Warning", "Category is empty")
        return False

    return True

def add_book():
    book_id, title, author, year, category = get_book_form_data()

    if not validate_book_form(book_id, title, author, year, category):
        return

    book = Book(int(book_id), title, author, int(year), category)
    added = library.add_book(book)

    if added is False:
        messagebox.showwarning("Warning", "This ID already exists")
        return

    save_all()
    clear_entries(book_entries)
    refresh_books()

def delete_book():
    book_id = selected_book_id()

    if book_id is None:
        messagebox.showwarning("Warning", "Select a book")
        return

    answer = messagebox.askyesno("Delete", "Delete this book?")

    if answer is False:
        return

    deleted = library.delete_book(book_id)

    if deleted is False:
        messagebox.showwarning("Warning", "Book cannot be deleted")
        return

    save_all()
    clear_entries(book_entries)
    refresh_books()

def edit_book():
    old_id = selected_book_id()

    if old_id is None:
        messagebox.showwarning("Warning", "Select a book")
        return

    book_id, title, author, year, category = get_book_form_data()

    if not validate_book_form(book_id, title, author, year, category):
        return

    book = find_book(old_id)

    if book is None:
        return

    other_book = find_book(book_id)

    if other_book is not None and other_book != book:
        messagebox.showwarning("Warning", "This ID already exists")
        return

    old_book_id = book.book_id
    book.book_id = int(book_id)
    book.title = title
    book.author = author
    book.year = int(year)
    book.category = category

    for member in library.members:
        for number in range(len(member.borrowed_books)):
            if str(member.borrowed_books[number]) == str(old_book_id):
                member.borrowed_books[number] = book.book_id

    save_all()
    clear_entries(book_entries)
    refresh_books()
    refresh_members()

def show_books():
    search_entry.delete(0, tk.END)
    notebook.select(books_tab)
    refresh_books()

def get_member_form_data():
    member_id = member_id_entry.get().strip()
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    return member_id, name, phone, email

def validate_member_form(member_id, name, phone, email):
    if not validate_member_id(member_id):
        messagebox.showwarning("Warning", "Member ID is wrong")
        return False

    if not validate_name(name):
        messagebox.showwarning("Warning", "Name is wrong")
        return False

    if not validate_phone(phone):
        messagebox.showwarning("Warning", "Phone is wrong")
        return False

    if not validate_email(email):
        messagebox.showwarning("Warning", "Email is wrong")
        return False

    return True

def add_member():
    member_id, name, phone, email = get_member_form_data()

    if not validate_member_form(member_id, name, phone, email):
        return

    member = Member(int(member_id), name, phone, email)
    added = library.add_member(member)

    if added is False:
        messagebox.showwarning("Warning", "This ID already exists")
        return

    save_all()
    clear_entries(member_entries)
    refresh_members()

def delete_member():
    member_id = selected_member_id()

    if member_id is None:
        messagebox.showwarning("Warning", "Select a member")
        return

    answer = messagebox.askyesno("Delete", "Delete this member?")

    if answer is False:
        return

    deleted = library.delete_member(member_id)

    if deleted is False:
        messagebox.showwarning("Warning", "Member cannot be deleted")
        return

    save_all()
    clear_entries(member_entries)
    refresh_members()

def edit_member():
    old_id = selected_member_id()

    if old_id is None:
        messagebox.showwarning("Warning", "Select a member")
        return

    member_id, name, phone, email = get_member_form_data()

    if not validate_member_form(member_id, name, phone, email):
        return

    member = find_member(old_id)

    if member is None:
        return

    other_member = find_member(member_id)

    if other_member is not None and other_member != member:
        messagebox.showwarning("Warning", "This ID already exists")
        return

    member.member_id = int(member_id)
    member.name = name
    member.phone = phone
    member.email = email

    save_all()
    clear_entries(member_entries)
    refresh_members()

def show_members():
    search_entry.delete(0, tk.END)
    notebook.select(members_tab)
    refresh_members()

def process_borrow(book_id, member_id):
    if not validate_book_id(book_id):
        messagebox.showwarning("Warning", "Book ID is wrong")
        return False

    if not validate_member_id(member_id):
        messagebox.showwarning("Warning", "Member ID is wrong")
        return False

    result = library.borrow_book(int(member_id), int(book_id))

    if result is False:
        messagebox.showwarning("Warning", "Borrow operation failed")
        return False

    save_all()
    refresh_books()
    refresh_members()
    return True

def borrow_book():
    book_id = simpledialog.askstring("Borrow", "Book ID:")

    if book_id is None:
        return

    member_id = simpledialog.askstring("Borrow", "Member ID:")

    if member_id is None:
        return

    process_borrow(book_id, member_id)

def process_return(book_id, member_id):
    if not validate_book_id(book_id):
        messagebox.showwarning("Warning", "Book ID is wrong")
        return False

    if not validate_member_id(member_id):
        messagebox.showwarning("Warning", "Member ID is wrong")
        return False

    result = library.return_book(int(member_id), int(book_id))

    if result is False:
        messagebox.showwarning("Warning", "Return operation failed")
        return False

    save_all()
    refresh_books()
    refresh_members()
    return True


def return_book():
    book_id = simpledialog.askstring("Return", "Book ID:")

    if book_id is None:
        return

    member_id = simpledialog.askstring("Return", "Member ID:")

    if member_id is None:
        return

    process_return(book_id, member_id)


def search():
    text = search_entry.get().strip().lower()
    active_tab = notebook.index(notebook.select())

    if text == "":
        if active_tab == 0:
            refresh_books()
        else:
            refresh_members()
        return

    if active_tab == 0:
        found_books = []

        for book in library.books:
            all_text = str(book.book_id)
            all_text = all_text + " " + book.title
            all_text = all_text + " " + book.author
            all_text = all_text + " " + str(book.year)
            all_text = all_text + " " + book.category

            if text in all_text.lower():
                found_books.append(book)

        refresh_books(found_books)
    else:
        found_members = []

        for member in library.members:
            all_text = str(member.member_id)
            all_text = all_text + " " + member.name
            all_text = all_text + " " + member.phone
            all_text = all_text + " " + member.email

            if text in all_text.lower():
                found_members.append(member)

        refresh_members(found_members)


def sort_data():
    choice = sort_combo.get()
    active_tab = notebook.index(notebook.select())

    if active_tab == 0:
        if choice == "ID":
            library.books.sort(key=lambda book: book.book_id)
        elif choice == "Title":
            library.books.sort(key=lambda book: book.title.lower())
        elif choice == "Author":
            library.books.sort(key=lambda book: book.author.lower())
        elif choice == "Year":
            library.books.sort(key=lambda book: book.year)
        elif choice == "Category":
            library.books.sort(key=lambda book: book.category.lower())

        refresh_books()
    else:
        if choice == "ID":
            library.members.sort(key=lambda member: member.member_id)
        elif choice == "Name":
            library.members.sort(key=lambda member: member.name.lower())
        elif choice == "Phone":
            library.members.sort(key=lambda member: member.phone)
        elif choice == "Email":
            library.members.sort(key=lambda member: member.email.lower())

        refresh_members()


def update_sort_options(event=None):
    active_tab = notebook.index(notebook.select())

    if active_tab == 0:
        sort_combo["values"] = ("ID", "Title", "Author", "Year", "Category")
    else:
        sort_combo["values"] = ("ID", "Name", "Phone", "Email")

    sort_combo.set("ID")


def statistics():
    data = library.statistics()

    text = "Total books: " + str(data["Total Books"])
    text = text + "\nAvailable books: " + str(data["Available Books"])
    text = text + "\nBorrowed books: " + str(data["Borrowed Books"])
    text = text + "\nTotal members: " + str(data["Total Members"])
    text = text + "\nMost category: " + str(data["Most Category"])

    messagebox.showinfo("Statistics", text)


def exit_program():
    answer = messagebox.askyesno("Exit", "Save and exit?")

    if answer:
        save_all()
        window.destroy()

title_label = tk.Label(window, text="LIBRARY MANAGEMENT", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

notebook = ttk.Notebook(window)
notebook.pack(fill="both", expand=True, padx=10)

books_tab = ttk.Frame(notebook)
members_tab = ttk.Frame(notebook)
notebook.add(books_tab, text="Books")
notebook.add(members_tab, text="Members")

book_form = ttk.LabelFrame(books_tab, text="Book information")
book_form.pack(fill="x", padx=10, pady=10)

ttk.Label(book_form, text="ID").grid(row=0, column=0, padx=5, pady=5)
book_id_entry = ttk.Entry(book_form, width=10)
book_id_entry.grid(row=1, column=0, padx=5, pady=5)

ttk.Label(book_form, text="Title").grid(row=0, column=1, padx=5, pady=5)
title_entry = ttk.Entry(book_form, width=24)
title_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(book_form, text="Author").grid(row=0, column=2, padx=5, pady=5)
author_entry = ttk.Entry(book_form, width=20)
author_entry.grid(row=1, column=2, padx=5, pady=5)

ttk.Label(book_form, text="Year").grid(row=0, column=3, padx=5, pady=5)
year_entry = ttk.Entry(book_form, width=10)
year_entry.grid(row=1, column=3, padx=5, pady=5)

ttk.Label(book_form, text="Category").grid(row=0, column=4, padx=5, pady=5)
category_entry = ttk.Entry(book_form, width=18)
category_entry.grid(row=1, column=4, padx=5, pady=5)

book_entries = [
    book_id_entry,
    title_entry,
    author_entry,
    year_entry,
    category_entry
]

book_buttons = ttk.Frame(books_tab)
book_buttons.pack(fill="x", padx=10, pady=5)

ttk.Button(book_buttons, text="Add", command=add_book).pack(side="left", padx=4)
ttk.Button(book_buttons, text="Edit", command=edit_book).pack(side="left", padx=4)
ttk.Button(book_buttons, text="Delete", command=delete_book).pack(side="left", padx=4)
ttk.Button(book_buttons, text="Show all", command=show_books).pack(side="left", padx=4)

book_columns = ("id", "title", "author", "year", "category", "available")
book_tree = ttk.Treeview(books_tab, columns=book_columns, show="headings")
book_tree.heading("id", text="ID")
book_tree.heading("title", text="Title")
book_tree.heading("author", text="Author")
book_tree.heading("year", text="Year")
book_tree.heading("category", text="Category")
book_tree.heading("available", text="Available")
book_tree.column("id", width=60)
book_tree.column("title", width=200)
book_tree.column("author", width=160)
book_tree.column("year", width=70)
book_tree.column("category", width=130)
book_tree.column("available", width=80)
book_tree.pack(fill="both", expand=True, padx=10, pady=10)
book_tree.bind("<<TreeviewSelect>>", fill_book_form)

member_form = ttk.LabelFrame(members_tab, text="Member information")
member_form.pack(fill="x", padx=10, pady=10)

ttk.Label(member_form, text="ID").grid(row=0, column=0, padx=5, pady=5)
member_id_entry = ttk.Entry(member_form, width=10)
member_id_entry.grid(row=1, column=0, padx=5, pady=5)

ttk.Label(member_form, text="Name").grid(row=0, column=1, padx=5, pady=5)
name_entry = ttk.Entry(member_form, width=22)
name_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(member_form, text="Phone").grid(row=0, column=2, padx=5, pady=5)
phone_entry = ttk.Entry(member_form, width=18)
phone_entry.grid(row=1, column=2, padx=5, pady=5)

ttk.Label(member_form, text="Email").grid(row=0, column=3, padx=5, pady=5)
email_entry = ttk.Entry(member_form, width=28)
email_entry.grid(row=1, column=3, padx=5, pady=5)

member_entries = [
    member_id_entry,
    name_entry,
    phone_entry,
    email_entry
]

member_buttons = ttk.Frame(members_tab)
member_buttons.pack(fill="x", padx=10, pady=5)

ttk.Button(member_buttons, text="Add", command=add_member).pack(side="left", padx=4)
ttk.Button(member_buttons, text="Edit", command=edit_member).pack(side="left", padx=4)
ttk.Button(member_buttons, text="Delete", command=delete_member).pack(side="left", padx=4)
ttk.Button(member_buttons, text="Show all", command=show_members).pack(side="left", padx=4)
member_columns = ("id", "name", "phone", "email", "books")
member_tree = ttk.Treeview(members_tab, columns=member_columns, show="headings")
member_tree.heading("id", text="ID")
member_tree.heading("name", text="Name")
member_tree.heading("phone", text="Phone")
member_tree.heading("email", text="Email")
member_tree.heading("books", text="Borrowed books")
member_tree.column("id", width=60)
member_tree.column("name", width=180)
member_tree.column("phone", width=130)
member_tree.column("email", width=230)
member_tree.column("books", width=180)
member_tree.pack(fill="both", expand=True, padx=10, pady=10)
member_tree.bind("<<TreeviewSelect>>", fill_member_form)
bottom_frame = ttk.Frame(window)
bottom_frame.pack(fill="x", padx=10, pady=10)

search_entry = ttk.Entry(bottom_frame, width=20)
search_entry.pack(side="left", padx=4)
ttk.Button(bottom_frame, text="Search", command=search).pack(side="left", padx=4)

sort_combo = ttk.Combobox(bottom_frame, width=12, state="readonly")
sort_combo.pack(side="left", padx=4)
sort_combo.set("ID")
ttk.Button(bottom_frame, text="Sort", command=sort_data).pack(side="left", padx=4)
ttk.Button(bottom_frame, text="Borrow", command=borrow_book).pack(side="left", padx=12)
ttk.Button(bottom_frame, text="Return", command=return_book).pack(side="left", padx=4)
ttk.Button(bottom_frame, text="Statistics", command=statistics).pack(side="left", padx=12)
ttk.Button(bottom_frame, text="Exit", command=exit_program).pack(side="right", padx=4)
status_label = tk.Label(window, textvariable=status_text, anchor="w")
status_label.pack(fill="x", padx=10, pady=(0, 5))
notebook.bind("<<NotebookTabChanged>>", update_sort_options)
window.protocol("WM_DELETE_WINDOW", exit_program)
update_sort_options()
refresh_books()
refresh_members()
if __name__ == "__main__":
    window.mainloop()
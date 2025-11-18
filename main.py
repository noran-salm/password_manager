from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = (
        [random.choice(letters) for _ in range(nr_letters)] +
        [random.choice(symbols) for _ in range(nr_symbols)] +
        [random.choice(numbers) for _ in range(nr_numbers)]
    )

    random.shuffle(password_list)
    password = "".join(password_list)
    pass_entry.delete(0, END)
    pass_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web_data = website_entry.get().strip()
    email_data = email_entry.get().strip()
    pass_data = pass_entry.get().strip()

    if not web_data or not email_data or not pass_data:
        messagebox.showinfo(title="Error", message="Please don’t leave any field empty.")
        return

    if "@" not in email_data or "." not in email_data:
        messagebox.showinfo(title="Invalid Email", message="Please enter a valid email address.")
        return

    new_data = {
        web_data: {
            "Email/Username": email_data,
            "Password": pass_data,
        }
    }

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        with open("data.json", "w") as file:
            json.dump(new_data, file, indent=4)
    else:
        data.update(new_data)
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
    finally:
        website_entry.delete(0, END)
        pass_entry.delete(0, END)

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def srch():
    web_data = website_entry.get().strip()
    if not web_data:
        messagebox.showinfo(title="Input Error", message="Please enter a website to search.")
        return

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
    else:
        if web_data in data:
            srch_email = data[web_data]["Email/Username"]
            srch_pass = data[web_data]["Password"]
            messagebox.showinfo(title=web_data, message=f"Email: {srch_email}\nPassword: {srch_pass}")
        else:
            messagebox.showinfo(title="Not Found", message=f"No details for '{web_data}' found.")
    finally:
        website_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

# Main Frame (to center everything)
main_frame = Frame(window)
main_frame.grid(row=0, column=0)

# Logo
canvas = Canvas(main_frame, width=200, height=200, highlightthickness=0)
try:
    logo_img = PhotoImage(file="logo.png")
    canvas.create_image(100, 100, image=logo_img)
except:
    pass
canvas.grid(column=1, row=0, pady=10)

# Labels
Label(main_frame, text="Website:").grid(column=0, row=1, sticky="e")
Label(main_frame, text="Email/Username:").grid(column=0, row=2, sticky="e")
Label(main_frame, text="Password:").grid(column=0, row=3, sticky="e")

# Entries
website_entry = Entry(main_frame, width=24)
website_entry.grid(column=1, row=1, sticky="w")
website_entry.focus()

email_entry = Entry(main_frame, width=38)
email_entry.grid(column=1, row=2, columnspan=2, sticky="w")
email_entry.insert(0, "@gmail.com")

pass_entry = Entry(main_frame, width=24)
pass_entry.grid(column=1, row=3, sticky="w")

# Buttons
Button(main_frame, text="Search", width=14, command=srch).grid(column=2, row=1, padx=5)
Button(main_frame, text="Generate Password", command=generate).grid(column=2, row=3, padx=5)
Button(main_frame, text="Add", width=38, command=save).grid(column=1, row=4, columnspan=2, pady=10)

window.mainloop()

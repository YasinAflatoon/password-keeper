from tkinter import *
from tkinter import messagebox
import random
import json


# ------- PASSWORD GENERATOR ------- #
def generate_pass():
    pass_entry.delete(0, END)
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
               'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_numbers = [random.choice(numbers) for _ in range(8)]
    password_letters = [random.choice(letters) for _ in range(5)]
    password_symbols = [random.choice(symbols) for _ in range(2)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    final = "".join(password_list)
    pass_entry.insert(0, final)


# ------- SAVE PASSWORD ------- #
def save():
    webpage = (web_entry.get()).strip()
    username = (user_entry.get()).strip()
    password = pass_entry.get()

    if webpage == "":
        messagebox.showerror(title="Empty Field", message='"Website/App" Field cannot be empty!')
    elif username == "":
        messagebox.showerror(title="Empty Field", message='"Username" Field cannot be empty!')
    elif password == "":
        messagebox.showerror(title="Empty Field", message='"Password" Field cannot be empty!')
    else:
        user_confirm = messagebox.askokcancel(title=webpage, message=f"Username: {username}\nPassword: {password}\n"
                                                                     f"Do You Want to Save This Login Info?")
        if user_confirm:
            new_info = {
                webpage: {
                    "username": username,
                    "password": password}
            }
            try:
                datafile = open("saved-passwords.json", mode="r")

            except FileNotFoundError:
                datafile = open("saved-passwords.json", mode="w")
                datafile.close()
            else:
                datafile.close()

            try:
                with open("saved-passwords.json", "r") as datafile:
                    file_content = json.load(datafile)

            except json.decoder.JSONDecodeError:
                with open("saved-passwords.json", "a") as datafile:
                    json.dump(new_info, datafile, indent=4)
            else:
                file_content.update(new_info)
                with open("saved-passwords.json", mode="w") as datafile:
                    json.dump(file_content, datafile, indent=4)

            messagebox.showinfo(title="Success!", message="Successfully Added!")
            web_entry.delete(0, END)
            pass_entry.delete(0, END)
            web_entry.focus()


def search():
    webpage = (web_entry.get()).strip()

    try:
        with open("saved-passwords.json", "r") as datafile:
            file_data = json.load(datafile)

    except FileNotFoundError:
        messagebox.showerror(title="Error!", message="Failed to detect a data file!\n"
                                                     "Please make sure you have added a login info to the app.")
    except json.decoder.JSONDecodeError:
        messagebox.showwarning(title="Not Found!", message=f"No match found for \"{webpage}\"!\n"
                                                           f"Check for any possible typos if you are sure you have "
                                                           f"added this login info.")
    else:
        item_found = False
        for key in file_data:
            if key.lower() == webpage.lower():
                messagebox.showinfo(title=key, message=f"Username: {file_data[key]['username']}\n"
                                                       f"Password: {file_data[key]['password']}")
                item_found = True
                break

        if not item_found:
            messagebox.showwarning(title="Not Found!", message=f"No login data found for \"{webpage}\"!\n"
                                                               f"Check for any possible typos if you are sure you have "
                                                               f"added this login info.")


# ------- UI SETUP ------- #

window = Tk()
window.title("Aflatoon's Password Manager.")
# window.minsize(width=400, height=400)
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

website = Label(text="Website/App:")
website.grid(row=1, column=0)

user_label = Label(text="Username/Email:")
user_label.grid(row=2, column=0)

pass_label = Label(text="Password:")
pass_label.grid(row=3, column=0)

web_entry = Entry(width=35)
web_entry.grid(row=1, column=1, columnspan=2)
web_entry.focus()

user_entry = Entry(width=35)
user_entry.grid(row=2, column=1, columnspan=2)

pass_entry = Entry(width=35)
pass_entry.grid(row=3, column=1)

pass_gen = Button(text="Generate Password", command=generate_pass)
pass_gen.grid(row=3, column=3)

add_button = Button(text="Add", width=30, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", command=search)
search_button.grid(row=1, column=3)

window.mainloop()

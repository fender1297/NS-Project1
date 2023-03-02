from tkinter import *
from tkinter import messagebox
from password import Password
import json
import rsa

# Colors
WHITE = "#F9F9F9"
RED = "#c0392b"

# Font Family
FONT = ("Raleway", 9, "bold")


# Clear all fields
def clear_all():
    website_input.delete(0, END)
    email_username_input.delete(0, END)
    email_username_input.insert(0, "demo@email.com")
    password_input.delete(0, END)


# Search password
def search_password():
    search_data = website_input.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showerror(title="No data found",
                             message="There is no data in the database.")
        website_input.delete(0, END)
    else:
        if search_data in data:
            email = data[search_data]["email"]
            password = data[search_data]["password"]
            email_username_input.delete(0, END)
            password_input.delete(0, END)
            email_username_input.insert(0, email)
            password_input.insert(0, password)
            messagebox.showinfo(title=f"{website_input.get()}", message=f"Email: {email}\nPassword: {password}")
            search_button.clipboard_clear()
            search_button.clipboard_append(password)
        else:
            messagebox.showerror(title="Website not found",
                                 message="The website you searched can not be found, please try again.")
    finally:
        website_input.delete(0, END)
        password_input.delete(0, END)


# Generate random password
def generate_password():
    random_password = Password().create_password()
    if password_input.get() == "":
        password_input.insert(0, random_password)
        pass_gen_button.clipboard_append(random_password)
    else:
        password_input.delete(0, END)
        pass_gen_button.clipboard_clear()
        password_input.insert(0, random_password)
        pass_gen_button.clipboard_append(random_password)


# Add passwords to data.json
def add_password():
    website = website_input.get()
    email_username = email_username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email_username,
            "password": password,
        }
    }

    if website != "" and email_username != "" and password != "":
        correct_info = messagebox.askokcancel(title=website, message=f"These are the details you have entered:\n"
                                                                     f"Email: {email_username}\nPassword: {password}\n"
                                                                     f"Is it OK to save?")
        if correct_info:
            try:
                with open("data.json", mode="r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
                    # Updating old data with new data
                    data.update(new_data)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                with open("data.json", mode="w") as data_file:
                    # Saving the updated data
                    json.dump(new_data, data_file, indent=4)
            else:
                with open("data.json", mode="w") as data_file:
                    # Saving the updated data
                    json.dump(data, data_file, indent=4)
            finally:
                website_input.delete(0, END)
                email_username_input.delete(0, END)
                email_username_input.insert(0, "demo@email.com")
                password_input.delete(0, END)
    else:
        messagebox.showerror(title="Insufficient information", message="Please don't leave any fields empty")


# Root object definition
root = Tk()
root.title("Password Manager")
root.config(padx=40, pady=40, bg=WHITE)
root.resizable(width=False, height=False)



# Widgets
# Website label
website_label = Label(text="Website:", font=FONT, bg=WHITE, fg=RED)
website_input = Entry(width=25, highlightbackground=RED, highlightthickness=1, font=FONT)
website_input.focus()

# Email/Username label
email_username_label = Label(text="Email/Username:", font=FONT, bg=WHITE, fg=RED)
email_username_input = Entry(width=44, highlightbackground=RED, highlightthickness=1, font=FONT)
email_username_input.insert(0, "demo@email.com")

# Password label
password_label = Label(text="Password:", font=FONT, bg=WHITE, fg=RED)
password_input = Entry(width=25, highlightbackground=RED, highlightthickness=1, font=FONT)

# Buttons
clear_all_button = Button(text="Clear All", font=("Raleway", 9, "bold"), fg="white", bg=RED,
                          width=44, command=clear_all)
search_button = Button(text="Search", font=("Raleway", 9, "bold"), fg="white", bg=RED,
                       width=16, command=search_password)
pass_gen_button = Button(text="Generate Password", font=("Raleway", 9, "bold"), fg="white", bg=RED,
                         command=generate_password)
add_button = Button(text="Add Password", font=("Raleway", 9, "bold"), bg=RED, fg="white", width=44,
                    command=add_password)

# Grids
website_label.grid(row=1, column=0)
website_input.grid(row=1, column=1)
email_username_label.grid(row=2, column=0)
email_username_input.grid(row=2, column=1, columnspan=2, sticky="e", pady=2)
password_label.grid(row=3, column=0)
password_input.grid(row=3, column=1)
clear_all_button.grid(row=5, column=0, columnspan=3, sticky="e", pady=2)
search_button.grid(row=1, column=2, pady=2)
pass_gen_button.grid(row=3, column=2, sticky="e", pady=2)
add_button.grid(row=4, column=0, columnspan=3, sticky="e", pady=2)

# Root mainloop
root.mainloop()
import os
from tkinter import *
from tkinter import ttk
from CTkTable import *
import customtkinter as ctk
import sqlite3 as sql
from PIL import Image, ImageTk, ImageFilter
from CTkMessagebox import CTkMessagebox as mb

db = sql.connect("database.db")

if db:
    print(">>> Connected to Database!")
else:
    print(">>> Error Connecting to Database!")

csr = db.cursor()

csr.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='students';")
if csr.fetchone()[0] == 0:
    csr.execute('''CREATE TABLE students(
                    ID int(10) PRIMARY KEY,
                    Name varchar(20) NOT NULL,
                    Branch varchar(20) NOT NULL,
                    Mobile No varchar(10) NOT NULL)''')
    print(">>> Table 'students' Created Successfully")

csr.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='books_avl';")
if csr.fetchone()[0] == 0:
    csr.execute('''CREATE TABLE books_avl(
                    BookCode int(10) PRIMARY KEY,
                    BookName varchar(20) NOT NULL,
                    AuthorName varchar(20) NOT NULL,
                    PubName varchar(20) NOT NULL,
                    PubYear int(4) NOT NULL)''')
    print(">>> Table 'books_avl' Created Successfully.")

csr.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='issued_books';")
if csr.fetchone()[0] == 0:
    csr.execute('''CREATE TABLE issued_books(
                    ID int(10) PRIMARY KEY,
                    BookCode int(10),
                    BookName varchar(20) NOT NULL,
                    AuthorName varchar(20) NOT NULL,
                    PubName varchar(20) NOT NULL,
                    PubYear int(4) NOT NULL,
                    FOREIGN KEY (BookCode) REFERENCES books_avl(BookCode))''')
    print(">>> Table 'issued_books' Created Successfully.")

# csr.execute("CREATE TABLE students(ID int(10) PRIMARY KEY, Name varchar(20) NOT NULL, Branch varchar(20) NOT NULL, Mobile No varchar(10) NOT NULL)")
# csr.execute("CREATE TABLE books_avl(BookCode int(10) PRIMARY KEY, BookName varchar(20) NOT NULL, AuthorName varchar(20) NOT NULL, PubName varchar(20) NOT NULL, PubYear int(4) NOT NULL)")
# csr.execute("CREATE TABLE issued_books(ID int(10) PRIMARY KEY, BookCode int(10), BookName varchar(20) NOT NULL, AuthorName varchar(20) NOT NULL, PubName varchar(20) NOT NULL, PubYear int(4) NOT NULL, FOREIGN KEY (BookCode) REFERENCES books_avl(BookCode))")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class IssueBook(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Issue Book")
        self.geometry("1850x1080")
        self.resizable(False, True)
        self.after(0, lambda:self.state('zoomed'))
        self.wm_iconbitmap(default='./assets/module_icon.ico')
        self.font = ctk.CTkFont('arial', 25, weight='bold')
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.img = ctk.CTkImage(Image.open(self.path + "/assets/tick.png"), size=(40, 40))
        self.hd = ctk.CTkLabel(self, text="Issue Book", font=('arial', 35, 'bold')).pack(padx=20, pady=20)
        self.lbl = ctk.CTkLabel(self, text="Student ID", font=self.font, anchor=ctk.CENTER).place(relx=.3, rely=.15)
        self.ent = ctk.CTkEntry(self, placeholder_text="Enter Student ID", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent.place(relx=.445, rely=.15)
        self.lbl2 = ctk.CTkLabel(self, text="Book Code", font=self.font, anchor=ctk.CENTER).place(relx=.3, rely=.25)
        self.ent2 = ctk.CTkEntry(self, placeholder_text="Enter Book Code", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent2.place(relx=.445, rely=.25)
        self.lbl3 = ctk.CTkLabel(self, text="Book Name", font=self.font, anchor=ctk.CENTER).place(relx=.3, rely=.35)
        self.ent3 = ctk.CTkEntry(self, placeholder_text="Enter Book Name", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent3.place(relx=.445, rely=.35)
        self.lbl4 = ctk.CTkLabel(self, text="Author Name", font=self.font, anchor=ctk.CENTER).place(relx=.3, rely=.45)
        self.ent4 = ctk.CTkEntry(self, placeholder_text="Enter Author Name", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent4.place(relx=.445, rely=.45)
        self.lbl5 = ctk.CTkLabel(self, text="Book Lang", font=self.font, anchor=ctk.CENTER).place(relx=.3, rely=.55)
        self.ent5 = ctk.CTkEntry(self, placeholder_text="Enter Book Language", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent5.place(relx=.445, rely=.55)
        self.lbl6 = ctk.CTkLabel(self, text="Issue Date", font=self.font, anchor=ctk.CENTER).place(relx=.3, rely=.65)
        self.ent6 = ctk.CTkEntry(self, placeholder_text="Enter Issue Date (YYYY-MM-DD)", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent6.place(relx=.445, rely=.65)
        self.lbl7 = ctk.CTkLabel(self, text="Return Date", font=self.font, anchor=ctk.CENTER).place(relx=.3, rely=.75)
        self.ent7 = ctk.CTkEntry(self, placeholder_text="Enter Return Date (YYYY-MM-DD)", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent7.place(relx=.445, rely=.75)
        self.btn = ctk.CTkButton(self, text="Issue Book", image=self.img, font=('arial', 20, 'bold'), command=self.issuebk, height=70, width=190).place(relx=.45, rely=.85)

    def issuebk(self):
        csr.execute("SELECT ID FROM students")
        id = csr.fetchall()
        print(self.ent.get())
        for x in id:
            if str(x) == (f"({self.ent.get()},)"):
                stat = "INSERT INTO issued_books VALUES(?, ?, ?, ?, ?, ?, ?)"
                val = (int(self.ent.get()), int(self.ent2.get()), self.ent3.get(), self.ent4.get(), self.ent5.get(), self.ent6.get(), self.ent7.get())
                csr.execute(stat, val)
                db.commit()
                print(f">>> Book Has Been Issued with Ref Student ID: {self.ent.get()}")
                mb(title="Success", message=f"Book Has Been Issued with Ref Student ID: {self.ent.get()}", icon="check", option_1="Ok")
                self.ent.delete(0, ctk.END)
                self.ent2.delete(0, ctk.END)
                self.ent3.delete(0, ctk.END)
                self.ent4.delete(0, ctk.END)
                self.ent5.delete(0, ctk.END)
                self.ent6.delete(0, ctk.END)
                self.ent7.delete(0, ctk.END)
                break
            elif self.ent.get() == "":
                mb(title="Warning", message=f"Enter Student ID", icon="warning", option_1="Ok")
                break
            elif self.ent2.get() == "":
                mb(title="Warning", message=f"Enter Book Code", icon="warning", option_1="Ok")
                break
            elif self.ent3.get() == "":
                mb(title="Warning", message=f"Enter Book Name", icon="warning", option_1="Ok")
                break
            elif self.ent4.get() == "":
                mb(title="Warning", message=f"Enter Author Name", icon="warning", option_1="Ok")
                break
            elif self.ent5.get() == "":
                mb(title="Warning", message=f"Enter Book Lang", icon="warning", option_1="Ok")
                break
            elif self.ent6.get() == "":
                mb(title="Warning", message=f"Enter Issue Date", icon="warning", option_1="Ok")
                break
            elif self.ent7.get() == "":
                mb(title="Warning", message=f"Enter Return Date", icon="warning", option_1="Ok")
                break
        else:
            mb(title="Error", message=f"Enter Valid Details", icon="cancel", option_1="Ok")

class ReturnBook(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Return Book")
        self.geometry("1920x1080")
        self.resizable(False, True)
        self.after(0, lambda:self.state('zoomed'))
        self.wm_iconbitmap(default='./assets/module_icon.ico')
        self.font = ctk.CTkFont('arial', 25, weight='bold')
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.img = ctk.CTkImage(Image.open(self.path + "/assets/cross.png"), size=(40, 40))
        self.hd = ctk.CTkLabel(self, text="Return Book", font=('arial', 35, 'bold')).pack(padx=20, pady=20)
        self.lbl = ctk.CTkLabel(self, text="Book Code", font=self.font, anchor=ctk.CENTER).place(relx=.33, rely=.18)
        self.ent = ctk.CTkEntry(self, placeholder_text="Enter Book Code", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent.place(relx=.445, rely=.18)
        self.btn = ctk.CTkButton(self, text="Return Book", image=self.img, font=('arial', 20, 'bold'), command=self.returnbk, height=70, width=190).place(relx=.435, rely=.28)
        self.bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.text_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        self.selected_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        self.tablestyle = ttk.Style()
        self.tablestyle.theme_use('default')
        self.tablestyle.configure("Treeview", highlightthickness=0, bd=0, font=('Arial', 15), rowheight=30, borderwidth=0)
        self.tablestyle.configure("Treeview.Heading", font=('Arial', 18, 'bold'), borderwidth=1, relief="solid")
        self.tablestyle.configure("Treeview", background=self.bg_color, foreground=self.text_color, fieldbackground=self.bg_color, borderwidth=2)
        self.table = ttk.Treeview(self, columns=("ID", "BookCode", "BookName", "AuthorName", "Lang","IssueDate", "ReturnDate"), show="headings", height=15)
        self.table.heading("ID", text="ID")
        self.table.heading("BookCode", text="Book Code")
        self.table.heading("BookName", text="Book Name")
        self.table.heading("AuthorName", text="Author Name")
        self.table.heading("Lang", text="Language")
        self.table.heading("IssueDate", text="Issue Date")
        self.table.heading("ReturnDate", text="Return Date")
        self.table.column("ID", anchor="center", width=50)
        self.table.column("BookCode", anchor="center")
        self.table.column("BookName", anchor="center", width=250)
        self.table.column("AuthorName", anchor="center", width=250)
        self.table.column("Lang", anchor="center")
        self.table.column("IssueDate", anchor="center")
        self.table.column("ReturnDate", anchor="center")
        self.table.place(x=280, y=400)
        try:
            stat = "SELECT * FROM issued_books"
            csr.execute(stat)
            res = csr.fetchall()
            for x in self.table.get_children():
                self.table.delete(x)
            for y in res:
                self.table.insert('', "end", values=y)
        except:
            mb(title="Error", message="Books Not Found", icon="cancel", option_1="OK")

    def returnbk(self):
        csr.execute("SELECT BookCode FROM issued_books")
        code = csr.fetchall()
        for x in code:
            if str(x) == (f"({self.ent.get()},)"):
                stat = "DELETE FROM issued_books WHERE BookCode=?"
                val = (int(self.ent.get()), )
                csr.execute(stat, val)
                db.commit()
                stat = "SELECT * FROM issued_books"
                csr.execute(stat)
                res = csr.fetchall()
                for y in self.table.get_children():
                    self.table.delete(y)
                for z in res:
                    self.table.insert('', "end", values=z)
                print(f">>> Book Has Been Returned with Ref Book Code: {self.ent.get()}")
                mb(title="Success", message=f"Book Has Been Returned with Ref Book Code: {self.ent.get()}", icon="check", option_1="Ok")
                self.ent.delete(0, ctk.END)
                break
            elif self.ent.get() == "":
                mb(title="Warning", message=f"Enter Book Code", icon="warning", option_1="Ok")
                break
        else:
            print(f"< ERROR > No Book Found with Book Code: {self.ent.get()}")
            mb(title="Error", message=f"No Book Found with Book Code: {self.ent.get()}", icon="cancel", option_1="Ok")

class AddStudent(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Upload Student Data")
        self.geometry("1920x1080")
        self.resizable(False, True)
        self.after(0, lambda:self.state('zoomed'))
        self.wm_iconbitmap(default='./assets/module_icon.ico')
        self.font = ctk.CTkFont('arial', 25, weight='bold')
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.img = ctk.CTkImage(Image.open(self.path + "/assets/tick.png"), size=(40, 40))
        self.label = ctk.CTkLabel(self, text="Upload Student Data", font=('arial', 35, 'bold')).pack(padx=20, pady=20)
        self.lbl = ctk.CTkLabel(self, text="Student ID", font=self.font, anchor=ctk.CENTER).place(relx=.34, rely=.2)
        self.ent = ctk.CTkEntry(self, placeholder_text="Enter Student ID", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent.place(relx=.5, rely=.2)
        self.lbl2 = ctk.CTkLabel(self, text="Student Name", font=self.font, anchor=ctk.CENTER).place(relx=.34, rely=.3)
        self.ent2 = ctk.CTkEntry(self, placeholder_text="Enter Student Name", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent2.place(relx=.5, rely=.3)
        self.lbl3 = ctk.CTkLabel(self, text="Student Branch", font=self.font, anchor=ctk.CENTER).place(relx=.34, rely=.4)
        self.ent3 = ctk.CTkEntry(self, placeholder_text="Enter Student Branch", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent3.place(relx=.5, rely=.4)
        self.lbl4 = ctk.CTkLabel(self, text="Student Mobile No", font=self.font, anchor=ctk.CENTER).place(relx=.34, rely=.5)
        self.ent4 = ctk.CTkEntry(self, placeholder_text="Enter Student Mobile No", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent4.place(relx=.5, rely=.5)
        self.btn = ctk.CTkButton(self, text="Upload Data", image=self.img, font=('arial', 20, 'bold'), command=self.addstud, height=70, width=190).place(relx=.45, rely=.6)

    def addstud(self):
        csr.execute("SELECT ID FROM students")
        data = csr.fetchall()
        for x in data:
            if str(x) == (f"({self.ent.get()},)"):
                print(f"Student Already Registered with Student ID: {self.ent.get()}")
                mb(title="Error", message=f"Student Already Registered with Student ID: {self.ent.get()}", icon="cancel", option_1="Ok")
            elif self.ent.get() == "":
                mb(title="Warning", message=f"Enter Student ID", icon="warning", option_1="Ok")
                break
            elif self.ent2.get() == "":
                mb(title="Warning", message=f"Enter Student Name", icon="warning", option_1="Ok")
                break
            elif self.ent3.get() == "":
                mb(title="Warning", message=f"Enter Student Branch", icon="warning", option_1="Ok")
                break
            elif self.ent4.get() == "":
                mb(title="Warning", message=f"Enter Student Mobile No", icon="warning", option_1="Ok")
                break
        else:
            # if str(x) != (f"({self.ent.get()},)"):
            stat = "INSERT INTO students VALUES(?, ?, ?, ?)"
            val = (int(self.ent.get(), ), self.ent2.get(), self.ent3.get(), self.ent4.get())
            csr.execute(stat,val)
            db.commit()
            print(f">>> Student Data Uploaded with Ref Student ID: {self.ent.get()}")
            mb(title="Success", message=f"Student Data Uploaded with Ref Student ID: {self.ent.get()}", icon="check", option_1="Ok")
            self.ent.delete(0, ctk.END)
            self.ent2.delete(0, ctk.END)
            self.ent3.delete(0, ctk.END)
            self.ent4.delete(0, ctk.END)

class DelStudent(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Delete Student Data")
        self.geometry("1920x1080")
        self.resizable(False, True)
        self.after(0, lambda:self.state('zoomed'))
        self.wm_iconbitmap(default='./assets/module_icon.ico')
        self.font = ctk.CTkFont('arial', 25, weight='bold')
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.img = ctk.CTkImage(Image.open(self.path + "/assets/cross.png"), size=(40, 40))
        self.img2 = ctk.CTkImage(Image.open(self.path + "/assets/search.png"), size=(40, 40))
        self.hd = ctk.CTkLabel(self, text="Delete Student Data", font=('arial', 35, 'bold')).pack(padx=20, pady=20)
        self.lbl = ctk.CTkLabel(self, text="Student ID", font=self.font, anchor=ctk.CENTER).place(relx=.33, rely=.18)
        self.ent = ctk.CTkEntry(self, placeholder_text="Enter Student ID", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent.place(relx=.445, rely=.18)
        self.btn = ctk.CTkButton(self, text="Remove Student", image=self.img, font=('arial', 20, 'bold'), command=self.delstud, height=60, width=170).place(relx=.435, rely=.28)
        self.bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.text_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        self.selected_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        self.tablestyle = ttk.Style()
        self.tablestyle.theme_use('default')
        self.tablestyle.configure("Treeview", highlightthickness=0, bd=0, font=('Arial', 15), rowheight=30, borderwidth=0)
        self.tablestyle.configure("Treeview.Heading", font=('Arial', 18, 'bold'), borderwidth=1, relief="solid")
        self.tablestyle.configure("Treeview", background=self.bg_color, foreground=self.text_color, fieldbackground=self.bg_color, borderwidth=2)
        self.table = ttk.Treeview(self, columns=("ID", "Name", "Branch", "Mobile No"), show="headings", height=15)
        self.table.heading("ID", text="ID")
        self.table.heading("Name", text="Name")
        self.table.heading("Branch", text="Branch")
        self.table.heading("Mobile No", text="Mobile No")
        self.table.column("ID", anchor="center", width=50)
        self.table.column("Name", anchor="center")
        self.table.column("Branch", anchor="center")
        self.table.column("Mobile No", anchor="center")
        self.table.place(x=660, y=400)
        try:
            stat = "SELECT * FROM students"
            csr.execute(stat)
            res = csr.fetchall()
            for x in res:
                self.table.insert('', "end", values=x)
        except:
            mb(title="Error", message="Books Not Found", icon="cancel", option_1="OK")

    def delstud(self):
        csr.execute("SELECT ID FROM students")
        id = csr.fetchall()
        for x in id:
            if str(x) == (f"({self.ent.get()},)"):
                stat = "DELETE FROM students WHERE ID=?"
                val = (int(self.ent.get()), )
                csr.execute(stat, val)
                db.commit()
                stat = "SELECT * FROM students"
                csr.execute(stat)
                res = csr.fetchall()
                for y in self.table.get_children():
                    self.table.delete(y)
                for z in res:
                    self.table.insert('', "end", values=z)
                print(f">>> Student Data Deleted with Ref Student ID: {self.ent.get()}")
                mb(title="Success", message=f"Student Data Deleted with Ref Student ID: {self.ent.get()}", icon="check", option_1="Ok")
                self.ent.delete(0, ctk.END)
                break
            elif self.ent.get() == "":
                mb(title="Warning", message=f"Enter Student ID", icon="warning", option_1="Ok")
                break
        else:
            print(f"< ERROR > No Student Registered with Student ID: {self.ent.get()}")
            mb(title="Error", message=f"No Student Registered with Student ID: {self.ent.get()}", icon="cancel", option_1="Ok")

class SearchStudent(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Search Student")
        self.geometry("1920x1080")
        self.resizable(False, True)
        self.after(0, lambda:self.state('zoomed'))
        self.wm_iconbitmap(default='./assets/module_icon.ico')
        self.font = ctk.CTkFont('arial', 25, weight='bold')
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.img = ctk.CTkImage(Image.open(self.path + "/assets/search.png"), size=(40, 40))
        self.hd = ctk.CTkLabel(self, text="Search Student", font=('arial', 35, 'bold')).place(x=650, y=50)
        self.lbl = ctk.CTkLabel(self, text="Student ID", font=self.font, anchor=ctk.CENTER).place(relx=.33, rely=.18)
        self.ent = ctk.CTkEntry(self, placeholder_text="Enter Student ID", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent.place(relx=.445, rely=.18)
        self.btn = ctk.CTkButton(self, text="Search Student", image=self.img, font=('arial', 20, 'bold'), command=self.searchstd, height=50, width=200).place(relx=.435, rely=.28)
        self.btn = ctk.CTkButton(self, text="Reset", font=('arial', 20, 'bold'), command=self.reset, height=50, width=70).place(relx=.585, rely=.28)
        self.bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.text_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        self.selected_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        self.tablestyle = ttk.Style()
        self.tablestyle.theme_use('default')
        self.tablestyle.configure("Treeview", highlightthickness=0, bd=0, font=('Arial', 15), rowheight=30, borderwidth=0)
        self.tablestyle.configure("Treeview.Heading", font=('Arial', 18, 'bold'), borderwidth=1, relief="solid")
        self.tablestyle.configure("Treeview", background=self.bg_color, foreground=self.text_color, fieldbackground=self.bg_color, borderwidth=2)
        self.table = ttk.Treeview(self, columns=("ID", "Name", "Branch", "Mobile No"), show="headings", height=15)
        self.table.heading("ID", text="ID")
        self.table.heading("Name", text="Name")
        self.table.heading("Branch", text="Branch")
        self.table.heading("Mobile No", text="Mobile No")
        self.table.column("ID", anchor="center", width=50)
        self.table.column("Name", anchor="center")
        self.table.column("Branch", anchor="center")
        self.table.column("Mobile No", anchor="center")
        self.table.place(x=660, y=400)
        try:
            stat = "SELECT * FROM students"
            csr.execute(stat)
            res = csr.fetchall()
            for x in res:
                self.table.insert('', "end", values=x)
        except:
            mb(title="Error", message="Books Not Found", icon="cancel", option_1="OK")

    def searchstd(self):
        try:
            id = int(self.ent.get())
            stat = "SELECT * FROM students WHERE ID=?"
            csr.execute(stat, (id,))
            res = csr.fetchone()
            if res:
                for x in self.table.get_children():
                    self.table.delete(x)
                self.table.insert('', "end", values=res)
                print(f">>> Student Has Been Found with Ref Student ID: {self.ent.get()}")
            else:
                print(f"< ERROR > No Student Registered with Student ID: {self.ent.get()}")
                mb(title="Error", message=f"No Student Registered with Student ID: {self.ent.get()}", icon="cancel", option_1="Ok")
        except:
            print("< ERROR > Enter Student ID Before Searching!")
            mb(title="Warning", message=f"Enter Student ID", icon="warning", option_1="Ok")

    def reset(self):
        stat = "SELECT * FROM students"
        csr.execute(stat)
        res = csr.fetchall()
        for x in self.table.get_children():
            self.table.delete(x)
        for y in res:
            self.table.insert('', "end", values=y)
        print(">>> Data Resetted for Students")
        self.ent.delete(0, ctk.END)

class BookIssued(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Issued Books")
        self.geometry("1920x1080")
        self.resizable(False, True)
        self.after(0, lambda:self.state('zoomed'))
        self.wm_iconbitmap(default='./assets/module_icon.ico')
        self.font = ctk.CTkFont('arial', 25, weight='bold')
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.img = ctk.CTkImage(Image.open(self.path + "/assets/search.png"), size=(40, 40))
        self.hd = ctk.CTkLabel(self, text="Issued Books", font=('arial', 35, 'bold')).place(x=650, y=50)
        self.lbl = ctk.CTkLabel(self, text="Student ID", font=self.font, anchor=ctk.CENTER).place(relx=.33, rely=.18)
        self.ent = ctk.CTkEntry(self, placeholder_text="Enter Student ID", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent.place(relx=.445, rely=.18)
        self.btn = ctk.CTkButton(self, text="Search Book", image=self.img, font=('arial', 20, 'bold'), command=self.searchbook, height=50, width=190).place(relx=.435, rely=.28)
        self.btn = ctk.CTkButton(self, text="Reset", font=('arial', 20, 'bold'), command=self.reset, height=50, width=70).place(relx=.585, rely=.28)
        self.bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.text_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        self.selected_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        self.tablestyle = ttk.Style()
        self.tablestyle.theme_use('default')
        self.tablestyle.configure("Treeview", highlightthickness=0, bd=0, font=('Arial', 15), rowheight=30, borderwidth=0)
        self.tablestyle.configure("Treeview.Heading", font=('Arial', 18, 'bold'), borderwidth=1, relief="solid")
        self.tablestyle.configure("Treeview", background=self.bg_color, foreground=self.text_color, fieldbackground=self.bg_color, borderwidth=2)
        self.table = ttk.Treeview(self, columns=("ID", "BookCode", "BookName", "AuthorName", "Lang", "IssueDate", "ReturnDate"), show="headings", height=15)
        self.table.heading("ID", text="ID")
        self.table.heading("BookCode", text="Book Code")
        self.table.heading("BookName", text="Book Name")
        self.table.heading("AuthorName", text="Author Name")
        self.table.heading("Lang", text="Language")
        self.table.heading("IssueDate", text="Issue Date")
        self.table.heading("ReturnDate", text="Return Date")
        self.table.column("ID", anchor="center", width=50)
        self.table.column("BookCode", anchor="center")
        self.table.column("BookName", anchor="center", width=250)
        self.table.column("AuthorName", anchor="center", width=250)
        self.table.column("Lang", anchor="center")
        self.table.column("IssueDate", anchor="center")
        self.table.column("ReturnDate", anchor="center")
        self.table.place(x=320, y=400)
        try:
            stat = "SELECT * FROM issued_books"
            csr.execute(stat)
            res = csr.fetchall()
            for x in res:
                self.table.insert('', "end", values=x)
        except:
            mb(title="Error", message="Books Not Found", icon="cancel", option_1="OK")

    def searchbook(self):
        try:
            id = int(self.ent.get())
            stat = "SELECT * FROM issued_books WHERE ID=?"
            csr.execute(stat, (id,))
            res = csr.fetchall()
            if res:
                for x in self.table.get_children():
                    self.table.delete(x)
                for y in res:
                    self.table.insert('', "end", values=y)
                print(f">>> Books Have Been Found with Ref Student ID: {self.ent.get()}")
            else:
                print(f"< ERROR > No Books Issued For Student ID: {self.ent.get()}")
                mb(title="Error", message=f"No Books Issued For Student ID: {self.ent.get()}", icon="cancel", option_1="Ok")
        except:
            print(f"< ERROR > Enter Student ID Before Searching!")
            mb(title="Warning", message="Enter Student ID", icon="warning", option_1="OK")

    def reset(self):
        stat = "SELECT * FROM issued_books"
        csr.execute(stat)
        res = csr.fetchall()
        for x in self.table.get_children():
            self.table.delete(x)
        for y in res:
            self.table.insert('', "end", values=y)
        print(">>> Data Resetted for Issued Books")
        self.ent.delete(0, ctk.END)

class BookAvl(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Books Available")
        self.geometry("1920x1080")
        self.resizable(False, True)
        self.after(0, lambda:self.state('zoomed'))
        self.wm_iconbitmap(default='./assets/module_icon.ico')
        self.font = ctk.CTkFont('arial', 25, weight='bold')
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.img = ctk.CTkImage(Image.open(self.path + "/assets/search.png"), size=(40, 40))
        self.hd = ctk.CTkLabel(self, text="Books Available", font=('arial', 35, 'bold')).place(x=650, y=50)
        self.opt = ctk.CTkOptionMenu(self, values=["Book Code", "Book Name", "Author"], font=('arial', 20, 'bold'), height=32, width=160)
        self.opt.place(relx=.335, rely=.18)
        self.opt.set("Choose")
        self.ent = ctk.CTkEntry(self, placeholder_text="Enter Value", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent.place(relx=.445, rely=.18)
        self.btn = ctk.CTkButton(self, text="Search Book", image=self.img, font=('arial', 20, 'bold'), command=self.search, height=50, width=190).place(relx=.435, rely=.28)
        self.btn = ctk.CTkButton(self, text="Reset", font=('arial', 20, 'bold'), height=50, width=70, command=self.reset).place(relx=.585, rely=.28)
        self.bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.text_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        self.selected_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        self.tablestyle = ttk.Style()
        self.tablestyle.theme_use('default')
        self.tablestyle.configure("Treeview", highlightthickness=0, bd=0, font=('Arial', 15), rowheight=30, borderwidth=0)
        self.tablestyle.configure("Treeview.Heading", font=('Arial', 18, 'bold'), borderwidth=1, relief="solid")
        self.tablestyle.configure("Treeview", background=self.bg_color, foreground=self.text_color, fieldbackground=self.bg_color, borderwidth=2)
        self.table = ttk.Treeview(self, columns=("BookCode", "BookName", "AuthorName", "PubName", "PubYear"), show="headings", height=15)
        self.table.heading("BookCode", text="Book Code")
        self.table.heading("BookName", text="Book Name")
        self.table.heading("AuthorName", text="Author")
        self.table.heading("PubName", text="Publication Name")
        self.table.heading("PubYear", text="Publication Year")
        self.table.column("BookCode", anchor="center")
        self.table.column("BookName", anchor="center")
        self.table.column("AuthorName", anchor="center")
        self.table.column("PubName", anchor="center", width=300)
        self.table.column("PubYear", anchor="center")
        self.table.place(x=430, y=400)
        try:
            stat = "SELECT * FROM books_avl"
            csr.execute(stat)
            res = csr.fetchall()
            for x in res:
                self.table.insert('', "end", values=x)
        except:
            mb(title="Error", message="Books Not Found", icon="cancel", option_1="OK")

    def search(self):
        if self.opt.get() == "Book Code":
            try:
                code = int(self.ent.get())
                try:
                    stat = "SELECT * FROM books_avl WHERE BookCode=?"
                    csr.execute(stat, (code,) )
                    res = csr.fetchone()
                    for x in self.table.get_children():
                        self.table.delete(x)
                    self.table.insert('', "end", values=res)
                    print(">>> Data Fetched From Book Code")
                except:
                    mb(title="Error", message=f"No Book Found with Ref Book Code: {self.ent.get()}", icon="cancel", option_1="OK")
            except:
                mb(title="Warning", message="Enter Valid Details", icon="warning", option_1="OK")
        elif self.opt.get() == "Book Name":
            if self.ent.get() == "":
                mb(title="Warning", message="Enter Valid Details", icon="warning", option_1="OK")
            else:
                try:
                    stat = "SELECT * FROM books_avl WHERE BookName=?"
                    name = self.ent.get()
                    csr.execute(stat, (name,))
                    res = csr.fetchall()
                    for x in self.table.get_children():
                        self.table.delete(x)
                    for y in res:
                        self.table.insert('', "end", values=y)
                    print(">>> Data Fetched From Book Name")
                except:
                    mb(title="Error", message=f"No Book Found with Ref Book Name: {self.ent.get()}", icon="cancel", option_1="OK")
        elif self.opt.get() == "Author":
            if self.ent.get() == "":
                mb(title="Warning", message="Enter Valid Details", icon="warning", option_1="OK")
            else:
                try:
                    stat = "SELECT * FROM books_avl WHERE AuthorName=?"
                    author = self.ent.get()
                    csr.execute(stat, (author,))
                    res = csr.fetchall()
                    for x in self.table.get_children():
                        self.table.delete(x)
                    for y in res:
                        self.table.insert('', "end", values=y)
                    print(">>> Data Fetched From Author")
                except:
                    mb(title="Error", message=f"No Book Found with Ref Author: {self.ent.get()}", icon="cancel", option_1="OK")
        else:
            mb(title="Error", message=f"Choose an Appropiate Option First", icon="warning", option_1="OK")

    def reset(self):
        stat = "SELECT * FROM books_avl"
        csr.execute(stat)
        res = csr.fetchall()
        for x in self.table.get_children():
            self.table.delete(x)
        for y in res:
            self.table.insert('', "end", values=y)
        print(">>> Data Resetted for Available Books")
        self.ent.delete(0, ctk.END)

class AddBook(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Books Available")
        self.geometry("1920x1080")
        self.resizable(False, True)
        self.after(0, lambda:self.state('zoomed'))
        self.wm_iconbitmap(default='./assets/module_icon.ico')
        self.font = ctk.CTkFont('arial', 25, weight='bold')
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.img = ctk.CTkImage(Image.open(self.path + "/assets/search.png"), size=(40, 40))
        self.hd = ctk.CTkLabel(self, text="Books Available", font=('arial', 35, 'bold')).place(x=650, y=50)
        self.opt = ctk.CTkOptionMenu(self, values=["Book Code", "Book Name", "Author"], font=('arial', 20, 'bold'), height=32, width=160)
        self.opt.place(relx=.335, rely=.18)
        self.opt.set("Choose")
        self.ent = ctk.CTkEntry(self, placeholder_text="Enter Value", font=('arial', 20, 'bold'), fg_color=("#3B8ED0", "#1F6AA5"), width=400)
        self.ent.place(relx=.445, rely=.18)
        self.btn = ctk.CTkButton(self, text="Search Book", image=self.img, font=('arial', 20, 'bold'), command=self.search, height=50, width=190).place(relx=.435, rely=.28)
        self.btn = ctk.CTkButton(self, text="Reset", font=('arial', 20, 'bold'), height=50, width=70, command=self.reset).place(relx=.585, rely=.28)
        self.bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.text_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        self.selected_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        self.tablestyle = ttk.Style()
        self.tablestyle.theme_use('default')
        self.tablestyle.configure("Treeview", highlightthickness=0, bd=0, font=('Arial', 15), rowheight=30, borderwidth=0)
        self.tablestyle.configure("Treeview.Heading", font=('Arial', 18, 'bold'), borderwidth=1, relief="solid")
        self.tablestyle.configure("Treeview", background=self.bg_color, foreground=self.text_color, fieldbackground=self.bg_color, borderwidth=2)
        self.table = ttk.Treeview(self, columns=("BookCode", "BookName", "AuthorName", "PubName", "PubYear"), show="headings", height=15)
        self.table.heading("BookCode", text="Book Code")
        self.table.heading("BookName", text="Book Name")
        self.table.heading("AuthorName", text="Author")
        self.table.heading("PubName", text="Publication Name")
        self.table.heading("PubYear", text="Publication Year")
        self.table.column("BookCode", anchor="center")
        self.table.column("BookName", anchor="center")
        self.table.column("AuthorName", anchor="center")
        self.table.column("PubName", anchor="center", width=300)
        self.table.column("PubYear", anchor="center")
        self.table.place(x=430, y=400)
        try:
            stat = "SELECT * FROM books_avl"
            csr.execute(stat)
            res = csr.fetchall()
            for x in res:
                self.table.insert('', "end", values=x)
        except:
            mb(title="Error", message="Books Not Found", icon="cancel", option_1="OK")

    def search(self):
        if self.opt.get() == "Book Code":
            try:
                code = int(self.ent.get())
                try:
                    stat = "SELECT * FROM books_avl WHERE BookCode=?"
                    csr.execute(stat, (code,) )
                    res = csr.fetchone()
                    for x in self.table.get_children():
                        self.table.delete(x)
                    self.table.insert('', "end", values=res)
                    print(">>> Data Fetched From Book Code")
                except:
                    mb(title="Error", message=f"No Book Found with Ref Book Code: {self.ent.get()}", icon="cancel", option_1="OK")
            except:
                mb(title="Warning", message="Enter Valid Details", icon="warning", option_1="OK")
        elif self.opt.get() == "Book Name":
            if self.ent.get() == "":
                mb(title="Warning", message="Enter Valid Details", icon="warning", option_1="OK")
            else:
                try:
                    stat = "SELECT * FROM books_avl WHERE BookName=?"
                    name = self.ent.get()
                    csr.execute(stat, (name,))
                    res = csr.fetchall()
                    for x in self.table.get_children():
                        self.table.delete(x)
                    for y in res:
                        self.table.insert('', "end", values=y)
                    print(">>> Data Fetched From Book Name")
                except:
                    mb(title="Error", message=f"No Book Found with Ref Book Name: {self.ent.get()}", icon="cancel", option_1="OK")
        elif self.opt.get() == "Author":
            if self.ent.get() == "":
                mb(title="Warning", message="Enter Valid Details", icon="warning", option_1="OK")
            else:
                try:
                    stat = "SELECT * FROM books_avl WHERE AuthorName=?"
                    author = self.ent.get()
                    csr.execute(stat, (author,))
                    res = csr.fetchall()
                    for x in self.table.get_children():
                        self.table.delete(x)
                    for y in res:
                        self.table.insert('', "end", values=y)
                    print(">>> Data Fetched From Author")
                except:
                    mb(title="Error", message=f"No Book Found with Ref Author: {self.ent.get()}", icon="cancel", option_1="OK")
        else:
            mb(title="Error", message=f"Choose an Appropiate Option First", icon="warning", option_1="OK")

    def reset(self):
        stat = "SELECT * FROM books_avl"
        csr.execute(stat)
        res = csr.fetchall()
        for x in self.table.get_children():
            self.table.delete(x)
        for y in res:
            self.table.insert('', "end", values=y)
        print(">>> Data Resetted for Available Books")
        self.ent.delete(0, ctk.END)

class App(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1920x1080")
        self.resizable(False, True)
        self.title("Library Management System")
        self.font = ctk.CTkFont('arial', 30, weight="bold")
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.open = ctk.CTkImage(dark_image=Image.open(self.path + "/bg/bkg.jpg"), size=(1550, 900))
        self.bkg = ctk.CTkLabel(self, image=self.open, text='').pack(padx=1, pady=1)
        self.img2 = ctk.CTkImage(Image.open(self.path + "/assets/issue.png"), size=(100, 100))
        self.img3 = ctk.CTkImage(Image.open(self.path + "/assets/return.png"), size=(100, 100))
        self.img4 = ctk.CTkImage(Image.open(self.path + "/assets/student.png"), size=(100, 100))
        self.img5 = ctk.CTkImage(Image.open(self.path + "/assets/del.png"), size=(100, 100))
        self.img6 = ctk.CTkImage(Image.open(self.path + "/assets/search.png"), size=(100, 100))
        self.img7 = ctk.CTkImage(Image.open(self.path + "/assets/check.png"), size=(100, 100))
        self.img8 = ctk.CTkImage(Image.open(self.path + "/assets/books.png"), size=(100, 100))
        self.lbl = ctk.CTkLabel(self, text="LIBRARY", font=('poppins', 105, 'bold'), bg_color="#002949")
        self.lbl.place(x=50, y=30)
        self.lbl2 = ctk.CTkLabel(self, text="MANAGEMENT", font=('poppins', 65, 'bold'), bg_color="#002949")
        self.lbl2.place(x=52, y=135)
        self.lbl2 = ctk.CTkLabel(self, text="SYSTEM", font=('poppins', 65, 'bold'), bg_color="#022A4E")
        self.lbl2.place(x=530, y=135)
        self.btn_1 = ctk.CTkButton(self, text="Issue Book", image=self.img2, anchor=ctk.CENTER, compound="top", width=250, height=230, command=self.open_issue, font=self.font, border_color="white", border_width=2, corner_radius=10, bg_color="#002949")
        self.btn_1.place(x=50, y=250)
        self.btn_2 = ctk.CTkButton(self, text="Return Book", image=self.img3, anchor=ctk.CENTER, compound="top", width=250, height=230, command=self.open_return, font=self.font, border_color="white", border_width=2, corner_radius=10, bg_color="#002949")
        self.btn_2.place(x=50, y=525)
        self.btn_3 = ctk.CTkButton(self, text="Add Student", image=self.img4, anchor=ctk.CENTER, compound="top", width=250, height=230, command=self.open_addstudent, font=self.font, border_color="white", border_width=2, corner_radius=10, bg_color="#002949")
        self.btn_3.place(x=350, y=250)
        self.btn_4 = ctk.CTkButton(self, text="Del Student", image=self.img5, anchor=ctk.CENTER, compound="top", width=250, height=230, command=self.open_delstudent, font=self.font, border_color="white", border_width=2, corner_radius=10, bg_color="#002949")
        self.btn_4.place(x=350, y=525)
        self.btn_5 = ctk.CTkButton(self, text="Search Student", image=self.img6, anchor=ctk.CENTER, compound="top", width=250, height=230, command=self.open_searchstudent, font=self.font, border_color="white", border_width=2, corner_radius=10, bg_color="#002949")
        self.btn_5.place(x=650, y=250)
        self.btn_6 = ctk.CTkButton(self, text="Issued Books", image=self.img7, anchor=ctk.CENTER, compound="top", width=250, height=230, command=self.open_bookissued, font=self.font, border_color="white", border_width=2, corner_radius=10, bg_color="#002949")
        self.btn_6.place(x=650, y=525)
        self.btn_7 = ctk.CTkButton(self, text="Books Avl", image=self.img8, anchor=ctk.CENTER, compound="top", width=250, height=230, command=self.open_bookavl, font=self.font, border_color="white", border_width=2, corner_radius=10, bg_color="#002949")
        self.btn_7.place(x=950, y=250)
        self.btn_7 = ctk.CTkButton(self, text="Add Book", image=self.img8, anchor=ctk.CENTER, compound="top", width=250, height=230, command=self.open_addbook, font=self.font, border_color="white", border_width=2, corner_radius=10, bg_color="#002949")
        self.btn_7.place(x=950, y=525)
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.issue_window = None
        self.return_window = None
        self.addstudent_window = None
        self.delstudent_window = None
        self.searchstudent_window = None
        self.bookavl_window = None
        self.bookissued_window = None
        self.addbook_window = None

    def open_issue(self):
        if self.issue_window is None or not self.issue_window.winfo_exists():
            self.issue_window = IssueBook(self)
            self.issue_window.focus()
        else:
            self.issue_window.focus()

    def open_return(self):
        if self.return_window is None or not self.return_window.winfo_exists():
            self.return_window = ReturnBook(self)
        else:
            self.return_window.focus()

    def open_addstudent(self):
        if self.addstudent_window is None or not self.addstudent_window.winfo_exists():
            self.addstudent_window = AddStudent(self)
            self.addstudent_window.focus()
        else:
            self.addstudent_window.focus()

    def open_delstudent(self):
        if self.delstudent_window is None or not self.delstudent_window.winfo_exists():
            self.delstudent_window = DelStudent(self)
            self.delstudent_window.focus()
        else:
            self.delstudent_window.focus()

    def open_searchstudent(self):
        if self.searchstudent_window is None or not self.searchstudent_window.winfo_exists():
            self.searchstudent_window = SearchStudent(self)
            self.searchstudent_window.focus()
        else:
            self.searchstudent_window.focus()

    def open_bookavl(self):
        if self.bookavl_window is None or not self.bookavl_window.winfo_exists():
            self.bookavl_window = BookAvl(self)
            self.bookavl_window.focus()
        else:
            self.bookavl_window.focus()
            
    def open_bookissued(self):
        if self.bookissued_window is None or not self.bookissued_window.winfo_exists():
            self.bookissued_window = BookIssued(self)
            self.bookissued_window.focus()
        else:
            self.bookissued_window.focus()

    def open_addbook(self):
        if self.addbook_window is None or not self.addbook_window.winfo_exists():
            self.addbook_window = AddBook(self)
            self.addbook_window.focus()
        else:
            self.addbook_window.focus()

    def close_window(self):
        res = mb(title="Exit?", message="Are you sure you want to close the program?", icon="question", option_1="Cancel", option_2="Yes")
        if res.get() == "Yes":
            print(">>> Program Exited!")
            self.destroy()

class Login(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("330x175")
        self.resizable(False, False)
        self.title("Login")
        self.font = ctk.CTkFont('arial', 15, weight="normal")
        self.lbl = ctk.CTkLabel(self, text="Username", font=self.font).place(relx=0.1, rely=0.12)
        self.user = ctk.CTkEntry(self, width=180, placeholder_text="Username", font=self.font)
        self.user.place(relx=0.36, rely=0.12)
        self.lbl2 = ctk.CTkLabel(self, text="Password", font=self.font).place(relx=0.1, rely=0.42)
        self.passwd = ctk.CTkEntry(self, width=180, show="*", placeholder_text="Password", font=self.font)
        self.passwd.place(relx=0.36, rely=0.42)
        self.btn = ctk.CTkButton(self, text="Login", height=35, command=self.login,font=("arial", 13, "bold"))
        self.btn.place(relx=0.28, rely=0.72)

    def login(self):
        if self.user.get() == "":
            mb(title="Warning", message="Enter Username", icon="warning", option_1="Ok")
        elif self.passwd.get() == "":
            mb(title="Warning", message="Enter Password", icon="warning", option_1="Ok")
        if (self.user.get() == "admin" and self.passwd.get()=="admin"):
            self.user.delete(0, ctk.END)
            self.passwd.delete(0, ctk.END)
            print(">>> Login Successful!")
            mb(title="Success", message="You Have Been Logined", icon="check", option_1="OK")
            app = App()
            app2 = Login()
            app.focus()
            app2.withdraw()
            app.after(0, lambda:app.state('zoomed'))
        else:
            self.user.delete(0, ctk.END)
            self.passwd.delete(0, ctk.END)
            mb(title="Error", message="Invalid Username or Password", icon="cancel", option_1="Retry")
            print(">>> Login Unsuccessful!")

if __name__ == "__main__":
    app = Login()
    # app.wm_iconbitmap(default='./assets/module_icon.ico')
    # app.after(0, lambda:app.state('zoomed'))
    app.mainloop()

from tkinter import *
from tkinter.ttk import Combobox
import os
import time
import smtplib
import csv


# the main GUI
class MainGUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg="#BBB")
        self.status = False
        self.contacts = []
        self.setupGUI()
        self.counter = 0

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def contacts(self):
        return self._contacts

    @contacts.setter
    def contacts(self, contacts):
        self._contacts = contacts

    # sets up GUI
    def setupGUI(self):
        # configure rows and columns
        for row in range(6):
            Grid.rowconfigure(self, row, weight=1)
        for col in range(2):
            Grid.columnconfigure(self, col, weight=1)

        self.pwr_btn = Button(self, text="Turn ON", bg="#F33", fg="#3F3", activebackground="#E33", activeforeground="#3E3", command=lambda: self.power())
        self.pwr_btn.grid(columnspan=2, sticky=N+S+E+W)

        phone_lbl = Label(self, text="Phone # (digits only): ", bg="#BBB")
        phone_lbl.grid(row=1, sticky=E)
        self.phone = StringVar()
        phone_entry = Entry(self, textvariable=self.phone)
        phone_entry.grid(row=1, column=1, sticky=E+W)

        mopro_lbl = Label(self, text="Mobile service provider: ", bg="#BBB")
        mopro_lbl.grid(row=2, sticky=E)
        self.mopro = StringVar()
        mopro_box = Combobox(self, textvariable=self.mopro)
        mopro_box['values'] = ('Sprint', 'Verizon', 'T-Mobile', 'AT&T')
        mopro_box.grid(row=2, column=1, sticky=E+W)

        email_lbl = Label(self, text="Gmail address: ", bg="#BBB")
        email_lbl.grid(row=3, sticky=E)
        self.email = StringVar()
        email_entry = Entry(self, textvariable=self.email)
        email_entry.grid(row=3, column=1, sticky=E+W)

        paswd_lbl = Label(self, text="Email password: ", bg="#BBB")
        paswd_lbl.grid(row=4, sticky=E)
        self.paswd = StringVar()
        paswd_entry = Entry(self, textvariable=self.paswd, show='*')
        paswd_entry.grid(row=4, column=1, sticky=E+W)

        add_info_btn = Button(self, bg="#EEE", text="Add new contact", activebackground="#DDD", command=lambda: self.addInfo())
        add_info_btn.grid(row=5, sticky=N+S+E+W)

        test_btn = Button(self, text="test send", command=lambda: self.test())
        test_btn.grid(row=5, column=1, sticky=N+S+E+W)

        self.pack(fill=BOTH, expand=1)

    # turns the program on/off
    def power(self):
        if self.status:
            cmd = 'sudo service motion stop'
            os.system(cmd)
            self.status = False
            self.pwr_btn.config(text="Turn ON", bg="#F33", fg="#3F3", activebackground="#E33", activeforeground="#3E3")
        else:
            cmd = 'sudo service motion start'
            os.system(cmd)
            self.status = True
            self.pwr_btn.config(text="Turn OFF", bg="#3F3", fg="#F33", activebackground="#3E3", activeforeground="#E33")

    # saves the contact information in the text boxes as a new contact
    def addInfo(self):
        to = self.phone.get()
        if self.mopro.get() == 'Sprint':
            to += "@messaging.sprintpcs.com"
        if self.mopro.get() == 'Verizon':
            to += "@vtext.com"
        if self.mopro.get() == 'T-Mobile':
            to += "@tmomail.net"
        if self.mopro.get() == 'AT&T':
            to += "@txt.att.net"
        email_user = self.email.get()
        password = self.paswd.get()
        new_info = {"recipient": to, "email_un": email_user, "email_pw": password}
        self.contacts.append(new_info)
        self.addToFile()
        print("Contact added.")
    def addToFile(self):
        with open('MotionDetectionContacts.csv', 'a+', newline='') as contact_file:
            fieldnames = ["recipient", "email_un", "email_pw"]
            add_contact = csv.DictWriter(contact_file, fieldnames=fieldnames)
            for i in self.contacts:
                add_contact.writerow(i)

    # tests sending a text to contacts
    def test(self):
        for contact in self.contacts:
            SUBJECT = 'Motion Detected!'
            TEXT = 'Your Raspberry Pi detected an intruder!'
            print("Sending text")
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(contact["email_un"], contact["email_pw"])
            header = 'To: ' + contact["recipient"] + '\n' + 'From: ' + contact["email_un"]
            header = header + '\n' + 'Subject: ' + SUBJECT + '\n'
            print(header)
            msg = header + '\n' + TEXT + '\n\n'
            server.sendmail(contact["email_un"], contact["recipient"], msg)
            server.quit()
            time.sleep(1)
            print("Text sent")


################
# Main Program #
################

# create the window
window = Tk()

# set the title for the window
window.title("Motion Camera Menu")

# generate the GUI
p = MainGUI(window)

# display the GUI and wait for the user to interact
window.mainloop()

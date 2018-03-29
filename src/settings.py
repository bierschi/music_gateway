from tkinter import *
from tkinter import messagebox
from definitions import ROOT_DIR
import json
import os
import errno


class Settings:

    def __init__(self):
        self.fields = 'host', 'port', 'username', 'password', 'topic_name'
        self.root = Tk()
        self.root.geometry("350x250")
        self.root.resizable(0, 0)
        self.center(self.root)
        ents = self.makeform(self.root, self.fields)
        self.root.bind('<Return>', (lambda event, e=ents: self.fetch(e)))
        b1 = Button(self.root, text='create conf file', command=(lambda e=ents: self.fetch(e)))
        b1.pack(side=TOP, padx=10, pady=10)
        b2 = Button(self.root, text='Quit', command=self.root.quit)
        b2.pack(side=TOP, padx=10, pady=10)
        self.root.mainloop()

    def center(self, toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def create_json(self, host, port, username, password, topic):
        conf_file = json.dumps({
            "MQTT": {
                "host": host,
                "port": port,
                "username": username,
                "password": password
            },
            "TOPIC_NAME": {
                "topic": topic
            }
        }, indent=4)
        try:
            os.chdir(ROOT_DIR)
            if not os.path.exists('configs'):
                os.makedirs('configs')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        with open('configs/configuration.json', 'w') as json_file:
            json_file.write(conf_file)

    def fetch(self, entries):

        for entry in entries:
            if entry[0] == 'host':
                host = entry[1].get()
            if entry[0] == 'port':
                port = entry[1].get()
            if entry[0] == 'username':
                username = entry[1].get()
            if entry[0] == 'password':
                password = entry[1].get()
            if entry[0] == 'topic_name':
                topic_name = entry[1].get()

        self.create_json(host, port, username, password, topic_name)

        messagebox.showinfo("Info", "Successfully created the configuration file. \n\n (changes can be made in music_gateway-1.0/configs/configuration.json)")
        self.root.quit()

    def makeform(self, root, fields):
        entries = []
        for field in fields:
            row = Frame(root)
            if field == 'password':
                ent = Entry(row, show='*')
            else:
                ent = Entry(row)
            lab = Label(row, width=15, text=field, anchor='w')
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries.append((field, ent))
        return entries

from Tkinter import *
import i3ipc

i3 = i3ipc.Connection()
wins = i3.get_tree().find_focused().workspace().leaves()
ids = [w.id for w in wins]
names = [w.name for w in wins]

# First create application class

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.pack()
        self.create_widgets()


    # Create main GUI window
    def create_widgets(self):
        self.search_var = StringVar()
        self.search_var.trace("w", self.update_list)
        self.entry = Entry(self, textvariable=self.search_var, width=120)
	self.nrows = 15
        self.lbox = Listbox(self, selectmode=SINGLE, activestyle='none', width=125, height=self.nrows)

        self.entry.grid(row=0, column=0, padx=10, pady=3)
        self.lbox.grid(row=1, column=0, padx=10, pady=3)

	self.lbox.bind_all('<Key>', self._key)

        self.update_list()
	self.lbox.focus_set()

    def update_list(self, *args):
        search_term = self.search_var.get()

        self.lbox.delete(0, END)

	self.idlut = []
	self.nit = 0
	self.aind = 0

        for j in range(len(names)):
                if all(map(lambda x: x in names[j].lower(), search_term.lower().split(' '))):
                    self.lbox.insert(END, names[j])
		    self.idlut.append(j)
		    self.nit += 1
	self.lbox.select_set(0)

    def _key(self, event):
	if event.keysym == "Escape":
	    self._quit()
	elif event.keysym == "Return":
	    self._ok()
	elif event.keysym == "BackSpace":
	    self.entry.delete(0,END)
	elif event.keysym == "Up":
	    self._seloffset(-1)
	elif event.keysym == "Down":
	    self._seloffset(1)
	elif event.keysym == "Prior":
	    self._seloffset(1-self.nrows)
	elif event.keysym == "Next":
	    self._seloffset(self.nrows-1)
	elif event.keysym == "Home":
	    self._seloffset(-self.nit)
	elif event.keysym == "End":
	    self._seloffset(self.nit)
	else:
	    self.entry.insert(END, event.char)

    def _ok(self, event=None):
	try:
		self.lbox.focus_set()
		ind = self.lbox.curselection()[0]
		value = ids[self.idlut[ind]]
		i3.command('[con_id=%s] focus' % value)
		self.master.destroy()
	except IndexError:
		self.value = None

    def _quit(self, event=None):
	self.master.destroy()

    def _seloffset(self, ofs, event=None):
	self.aind = max(0, min(self.aind+ofs, self.nit-1))	
	self.lbox.selection_clear(0,END)
	self.lbox.select_set(self.aind)

root = Tk()
root.title('i3 window search')
app = Application(master=root)
app.mainloop()

'''
Jiaming Li
masterjm@cs.washington.edu
A simple python GUI to practice with wxWidget
It will be awesome if you see any bad codes here and tell me about that :)
'''

import wx

# Frame class
class OuterFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(500,520))
        self.CreateStatusBar()

        filemenu = wx.Menu()
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "Default")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "This is a simple direcotry, you can add, search and delete " +
                "people from the directory, and you can also use your own directory file(.dir extension)", 
                "About Directory", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

# Control Panel class
class ControlPanel(wx.Panel):
    def __init__(self, parent):

    	# Initial variables
        self.contacts = {}
        self.group = "Default"
        self.name = ""
        self.num = ""

        wx.Panel.__init__(self, parent)

        # create sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=7, vgap=7)

        # First label
        self.add = wx.StaticText(self, label="Contacts")
        grid.Add(self.add, pos=(0,0))

        # The console text area
        self.console = wx.TextCtrl(self, size=(500,300), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Three buttons binded to different functions
        self.addButton = wx.Button(self, label="Add")
        self.Bind(wx.EVT_BUTTON, self.onAdd, self.addButton)
        self.searchButton = wx.Button(self, label="Search")
        self.Bind(wx.EVT_BUTTON, self.onSearch,self.searchButton)
        self.deleteButton = wx.Button(self, label = "Delete")
        self.Bind(wx.EVT_BUTTON, self.onDelete,self.deleteButton)
        self.displayButton = wx.Button(self, label = "Display")
        self.Bind(wx.EVT_BUTTON, self.onDisplay, self.displayButton)
        self.saveButton = wx.Button(self, label="Save")
        self.Bind(wx.EVT_BUTTON, self.onSave, self.saveButton)

        # Name and number
        self.lblname = wx.StaticText(self, label="Name :")
        self.lblnum = wx.StaticText(self, label="Number :")
        grid.Add(self.lblname, pos=(1,0))
        grid.Add(self.lblnum, pos=(2,0))
        self.editname = wx.TextCtrl(self, size=(140,-1))
        self.editnum = wx.TextCtrl(self, size=(140, -1))
        grid.Add(self.editname, pos=(1,1))
        grid.Add(self.editnum, pos=(2,1))
        self.Bind(wx.EVT_TEXT, self.updateName, self.editname)
        self.Bind(wx.EVT_TEXT, self.updateNum, self.editnum)

        # Combobox label
        self.label = wx.StaticText(self, label="Group :")
        grid.Add(self.label, pos=(3,0))

        # Combobox list
        self.groupList = ["Default", "Family", "Work"]
        self.groupComboBox = wx.ComboBox(self, size=(95, -1), choices=self.groupList, style=wx.CB_DROPDOWN)
        grid.Add(self.groupComboBox, pos=(3,1))

        # Bind functions
        self.Bind(wx.EVT_COMBOBOX, self.updateComboBox, self.groupComboBox)

        # Add sizers
        mainSizer.Add(self.console)
        mainSizer.Add(grid, 0, wx.ALL, 5)
        grid.Add(self.addButton, pos=(4,0))
        grid.Add(self.searchButton, pos=(4,1))
        grid.Add(self.deleteButton, pos=(5,0))
        grid.Add(self.displayButton, pos=(5,1))
        grid.Add(self.saveButton, pos=(5, 10))
        self.SetSizerAndFit(mainSizer)
        self.display()

    # Updates group whenever the client changes combobox
    def updateComboBox(self, event):
        self.group = event.GetString()
    
    # Updates name whenever the client enters a name
    def updateName(self, event):
    	self.name = event.GetString()

    # Updates number whenever the clients enters a number
    def updateNum(self, event):
    	self.num = event.GetString()

    # Deletes one entry from the directory
    # It's okay to delete only delete a group(e.g. work) and it
    # will still display default and family
    def onDelete(self, event):
    	if self.group in self.contacts[self.name]:
        	del self.contacts[self.name][self.group]
       		self.appendToConsole(self.contacts)

    # Adds one entry onto the directory
    def onAdd(self, event):
    	if self.name in self.contacts:
            self.contacts[self.name].update({self.group: self.num})
        else:
            self.contacts.update({self.name: {self.group: self.num}})

        self.appendToConsole(self.contacts)

    # Search someone and display the result
    def onSearch(self, event):
        self.console.Clear()
        if self.name in self.contacts:
            for key in self.contacts[self.name]:
		    	self.console.AppendText("Here is the result: \n\n")
		    	self.console.AppendText(self.name + "\n")
		    	self.console.AppendText("\t" + key + ": " + self.contacts[self.name][key]) 
        else:
            self.console.AppendText("I don't have " + name + "\nClick display to see directory")

    # Redisplay a contact
    def onDisplay(self, event):
    	self.appendToConsole(self.contacts)

    # Save the content to the file
    def onSave(self, event):
    	dirFile = open("contacts.dir", "w").close()
    	dirFile = open("contacts.dir", "w")
    	for item in sorted(self.contacts):
        	if (any(self.contacts[item].keys())):
	            for key in self.contacts[item]:
	            	dirFile.write(item + "::")
	                dirFile.write(key + "::" + self.contacts[item][key].rstrip("\n") + "\n")
	        else:
	        	del contacts[item]

	# Initial display
	# It saves everything in a dictionary to allow faster access
    def display(self):
        dirFile = open("contacts.dir", "r+")
        for line in dirFile:
            if not line.startswith('//'):
                elt = line.split(":")
                if elt[0] in self.contacts:
                    self.contacts[elt[0]].update({elt[1]: elt[2]})
                else:
                    self.contacts.update({elt[0]: {elt[1]: elt[2]}})
        self.appendToConsole(self.contacts)
        dirFile.close()

    # Print everything onto console
    def appendToConsole(self, contacts):
    	self.console.Clear()
    	self.console.AppendText("Here are all your contacts: \n")
        self.console.AppendText("(Sort alphabetically) \n\n")
        for item in sorted(contacts):
        	if (any(contacts[item].keys())):
	            self.console.AppendText(item + ":\n")
	            for key in contacts[item]:
	                self.console.AppendText("\t" + key + ": " + contacts[item][key].rstrip("\n") + "\n")
	            self.console.AppendText("\n")
	        else:
	        	del contacts[item]

# Start everything
app = wx.App(False)
frame = OuterFrame(None, title="Contacts")
panel = ControlPanel(frame)
frame.Show()
app.MainLoop()
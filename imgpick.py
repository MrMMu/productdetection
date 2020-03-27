import wx,os

class Pop(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Pop, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):

        wx.CallLater(100, self.ShowMessage)

        self.SetSize((300, 200))
        self.SetTitle('Message box')
        self.Centre()

    def ShowMessage(self):
        wx.MessageBox('All Done!', 'Info',
            wx.OK | wx.ICON_INFORMATION)

class TestFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        
        self.MaxImageSize = 500
        
        #b = wx.Button(self, -1, "SELECT DIRECTORY")
        #b.Bind(wx.EVT_BUTTON, self.button_browse_path_click)
        
        #self.tbox = wx.TextCtrl(self, size=(140, -1))
        self.lblname = wx.StaticText(self, label="Path:\n")
        self.Path=""
        self.KeepPath=""
        self.SkipPath=""
        
        self.button_browse_path_click(event=None)
        os.makedirs(self.KeepPath, exist_ok=True)
        os.makedirs(self.SkipPath, exist_ok=True)
        
        # there needs to be an "Images" directory with one or more jpegs in it in the
        # current working directory for this to work
        self.jpgs = GetJpgList(self.Path) # get all the jpegs in the Images directory
        print(self.jpgs)
        self.CurrentJpg = 0        
        
        # starting with an EmptyBitmap, the real one will get put there
        # by the call to .DisplayNext()
        self.Image = wx.StaticBitmap(self, bitmap=wx.EmptyBitmap(self.MaxImageSize, self.MaxImageSize))
        
        self.DisplayNext(event=None,action="keep")

        # Using a Sizer to handle the layout: I never use absolute positioning
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.lblname, 0, wx.LEFT | wx.ALL,10)

        # adding stretchable space before and after centers the image.
        box.Add((1,1),1)
        box.Add(self.Image, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.ADJUST_MINSIZE, 10)
        box.Add((1,1),1)

        self.SetSizerAndFit(box)
        
        wx.EVT_CLOSE(self, self.OnCloseWindow)          

    def DisplayNext(self, event=None,action="none"):
        # load the image
        
        if self.CurrentJpg==-99:
            print("Last one or only one")
            if action=="keep":
                newfilename=self.KeepPath+self.jpgs[-1].split("/")[-1]
            elif action=="skip":
                newfilename=self.SkipPath+self.jpgs[-1].split("/")[-1]
            else:
                exit()
            print(newfilename)
            os.rename(self.jpgs[-1],newfilename.replace("jpeg","jpg"))
            ex = Pop(None)
            #ex.ShowMessage()       
            #exit()
            
            
        print(self.CurrentJpg)
        print(self.jpgs[self.CurrentJpg])
        Img = wx.Image(self.jpgs[self.CurrentJpg], wx.BITMAP_TYPE_ANY)
        
        # scale the image, preserving the aspect ratio
        W = Img.GetWidth()
        H = Img.GetHeight()
        if W > H:
            NewW = self.MaxImageSize
            NewH = self.MaxImageSize * H / W
        else:
            NewH = self.MaxImageSize
            NewW = self.MaxImageSize * W / H
        Img = Img.Scale(NewW,NewH)
 
        # convert it to a wx.Bitmap, and put it on the wx.StaticBitmap
        self.Image.SetBitmap(wx.BitmapFromImage(Img))

        # You can fit the frame to the image, if you want.
        self.Fit()
        self.Layout()
        self.Refresh()
        
        if self.CurrentJpg>0:
            print(self.jpgs[self.CurrentJpg-1])
            if action=="keep":
                newfilename=self.KeepPath+self.jpgs[self.CurrentJpg-1].split("/")[-1]
            elif action=="skip":
                newfilename=self.SkipPath+self.jpgs[self.CurrentJpg-1].split("/")[-1]
            else:
                exit()
            print(newfilename)
            print(self.CurrentJpg)
            os.rename(self.jpgs[self.CurrentJpg-1],newfilename.replace("jpeg","jpg"))

        self.CurrentJpg += 1
        if self.CurrentJpg > len(self.jpgs) -1:
            self.CurrentJpg = -99    

    def OnCloseWindow(self, event):
        self.Destroy()

    def button_browse_path_click(self, event):
        dlg = wx.DirDialog(
                self,
                "Choose a directory:",
                style=wx.DD_DEFAULT_STYLE
            )
    
        if dlg.ShowModal() == wx.ID_OK:
            self.lblname.SetLabel("Path:\n"+dlg.GetPath()+"\n")
            self.Path=dlg.GetPath()
            self.KeepPath=self.Path+"/keep/"
            self.SkipPath=self.Path+"/skip/"
            print('You selected: %s\n' % dlg.GetPath())
    
        dlg.Destroy()
    
        if event is not None:
            event.Skip()    
        
        
        
def GetJpgList(dir):
    jpgs = [f for f in os.listdir(dir) if (f[-4:] == ".jpg" or f[-5:] == ".jpeg")]
    # print "JPGS are:", jpgs
    return [os.path.join(dir, f) for f in jpgs]

class App(wx.App):
    def OnInit(self):

        self.frame = TestFrame(None, -1, "LEFT to skip, RIGHT to keep!", wx.DefaultPosition,(550,200))
        self.panel = wx.Panel(self.frame)
        
        self.panel.Bind(wx.EVT_CHAR, self.OnKeyChar)
        
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
        return True
    
    def OnKeyChar(self, event):
        if event.KeyCode == 316:  #Right key
            print("KEEP")
            self.frame.DisplayNext(event=None,action="keep")
        elif event.KeyCode == 314:  #Left key
            print("SKIP")
            self.frame.DisplayNext(event=None,action="skip")
        #print(event.KeyCode)
        event.Skip()    

if __name__ == "__main__":
    app = App(0)
    app.MainLoop()
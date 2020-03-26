import wx,os

class TestFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        
        self.Bind(wx.EVT_CHAR, self.OnKeyChar)
        

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
        self.CurrentJpg = 0        
        
        # starting with an EmptyBitmap, the real one will get put there
        # by the call to .DisplayNext()
        self.Image = wx.StaticBitmap(self, bitmap=wx.EmptyBitmap(self.MaxImageSize, self.MaxImageSize))
        
        self.DisplayNextKeep()

        # Using a Sizer to handle the layout: I never use absolute positioning
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.lblname, 0, wx.LEFT | wx.ALL,10)

        # adding stretchable space before and after centers the image.
        box.Add((1,1),1)
        box.Add(self.Image, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.ADJUST_MINSIZE, 10)
        box.Add((1,1),1)

        self.SetSizerAndFit(box)
        
        wx.EVT_CLOSE(self, self.OnCloseWindow)
        
    def OnKeyChar(self, event):
        if event.KeyCode == 316:  #Right key
            print("KEEP")
            self.frame.DisplayNextKeep()
        elif event.KeyCode == 314:  #Left key
            print("SKIP")
        #print(event.KeyCode)
        event.Skip()            

    def DisplayNextKeep(self, event=None):
        # load the image
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
            newfilename=self.KeepPath+self.jpgs[self.CurrentJpg-1].split("/")[-1]
            print(newfilename)
            os.rename(self.jpgs[self.CurrentJpg-1],newfilename)

        self.CurrentJpg += 1
        if self.CurrentJpg > len(self.jpgs) -1:
            self.CurrentJpg = 0
            
    def DisplayNextSkip(self, event=None): 
        # load the image
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
            newfilename=self.SkipPath+self.jpgs[self.CurrentJpg-1].split("/")[-1]
            print(newfilename)
            os.rename(self.jpgs[self.CurrentJpg-1],newfilename)
            
        self.CurrentJpg += 1
        if self.CurrentJpg > len(self.jpgs) -1:
            self.CurrentJpg = 0        

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
    jpgs = [f for f in os.listdir(dir) if f[-4:] == ".jpg"]
    # print "JPGS are:", jpgs
    return [os.path.join(dir, f) for f in jpgs]

class App(wx.App):
    def OnInit(self):

        self.frame = TestFrame(None, -1, "LEFT to skip, RIGHT to keep!", wx.DefaultPosition,(550,200))
        self.panel = wx.Panel(self.frame)
        
        #self.panel.Bind(wx.EVT_KEY_UP, self.OnKeyDown)
        self.panel.Bind(wx.EVT_CHAR, self.OnKeyChar)
        
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
        return True
    
    def OnKeyChar(self, event):
        if event.KeyCode == 316:  #Right key
            print("KEEP")
            self.frame.DisplayNextKeep()
        elif event.KeyCode == 314:  #Left key
            print("SKIP")
            self.frame.DisplayNextSkip()
        #print(event.KeyCode)
        event.Skip()    

if __name__ == "__main__":
    app = App(0)
    app.MainLoop()
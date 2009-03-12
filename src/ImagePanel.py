import wx
import ImageTools
from Properties import Properties

p = Properties.getInstance()

class ImagePanel(wx.Panel):
    '''
    ImagePanels are wxPanels that display a wxBitmap and store multiple
    image channels which can be recombined to mix different bitmaps.
    '''
    def __init__(self, images, channel_map, parent, scale=1.0, brightness=1.0):
        """
        images -- list of numpy arrays
        channel_map -- list of strings naming the color to map each channel 
                       onto, e.g., ['red', 'green', 'blue']
        
        """
        self.chMap       = channel_map
        self.toggleChMap = channel_map[:]
        self.images      = images
        self.bitmap      = ImageTools.MergeToBitmap(images,
                                                    chMap=channel_map,
                                                    scale=scale,
                                                    brightness = brightness)   # displayed wx.Bitmap
        
        wx.Panel.__init__(self, parent, wx.NewId(), size=self.bitmap.Size)
        
        self.scale       = scale
        self.brightness  = brightness
        self.selected    = False
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        
    def OnPaint(self, evt):
        self.SetClientSize((self.bitmap.Width, self.bitmap.Height))
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self.bitmap, 0, 0)
        # Outline the whole image
        if self.selected:
            dc.BeginDrawing()
            dc.SetPen(wx.Pen("WHITE",1))
            dc.SetBrush(wx.Brush("WHITE", style=wx.TRANSPARENT))
            dc.DrawRectangle(0,0,self.bitmap.Width,self.bitmap.Height)
            dc.EndDrawing()
        return dc


    def UpdateBitmap(self):
        self.bitmap = ImageTools.MergeToBitmap(self.images,
                                               chMap = self.chMap,
                                               brightness = self.brightness,
                                               scale = self.scale)
        self.Refresh()
            
    
    def MapChannels(self, chMap):
        ''' Recalculates the displayed bitmap for a new channel-color map. '''
        self.chMap = chMap
        self.UpdateBitmap()
        

    def SetScale(self, scale):
        if scale != self.scale:
            self.scale = scale
            self.UpdateBitmap()
            self.SetClientSize((self.bitmap.Width, self.bitmap.Height))

        
    def SetBrightness(self, brightness):
        if brightness != self.brightness:
            self.brightness = brightness
            self.UpdateBitmap()

    

        
            



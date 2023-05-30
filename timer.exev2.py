import wx
import time
import winsound

def play_sound():
    # Generate a beep sound
    winsound.Beep(440, 1000)  # Adjust the frequency and duration as desired

class DraggableFrame(wx.Frame):
    def __init__(self, parent, title):
        style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.CLOSE_BOX)
        wx.Frame.__init__(self, parent, title=title, style=style | wx.FRAME_SHAPED)

        self.SetBackgroundColour("#7e97ad")
        self.SetSizeHints(360, 100, 360, 100)  # Set fixed size

        # Remove the title bar by hiding the system menu
        self.SetWindowStyleFlag(wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)

        # Create a custom-shaped region to simulate the title bar
        region = wx.Region()
        region.AddRectangle(0, 0, self.GetSize().width, 30)
        self.SetShape(region)

        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour("#7e97ad")

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.label = wx.StaticText(self.panel, label="距离休息还剩 25:00", style=wx.ALIGN_CENTER)
        font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.label.SetFont(font)
        self.label.SetForegroundColour("#edced0")

        sizer.AddStretchSpacer(1)
        sizer.Add(self.label, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.AddStretchSpacer(1)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        restart_button = wx.Button(self.panel, label="Restart")
        restart_button.Bind(wx.EVT_BUTTON, self.on_restart)
        restart_button.SetBackgroundColour("#7e97ad")
        restart_button.SetForegroundColour("#edced0")

        close_button = wx.Button(self.panel, label="Close")
        close_button.Bind(wx.EVT_BUTTON, self.on_close)
        close_button.SetBackgroundColour("#7e97ad")
        close_button.SetForegroundColour("#edced0")

        button_sizer.Add(restart_button, 0, wx.ALL, 5)
        button_sizer.AddSpacer(10)
        button_sizer.Add(close_button, 0, wx.ALL, 5)

        sizer.Add(button_sizer, 0, wx.CENTER | wx.BOTTOM, 10)

        self.panel.SetSizerAndFit(sizer)
        min_width, min_height = sizer.GetMinSize()
        scale_factor = 1.2  # Enlarge the window by 20%
        self.SetSize(int(min_width * scale_factor), int(min_height * scale_factor))

        self.countdown_duration = 25 * 60
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)

        self.restart()

        # Variables for tracking mouse movement and window position
        self.dragging = False
        self.window_pos = None
        self.mouse_pos = None

        # Bind mouse events
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.panel.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.panel.Bind(wx.EVT_MOTION, self.on_motion)

    def restart(self):
        self.start_time = time.time()
        self.end_time = self.start_time + self.countdown

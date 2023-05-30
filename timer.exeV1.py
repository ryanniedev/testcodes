import wx
import time
import winsound

def play_sound():
    # Generate a beep sound
    winsound.Beep(440, 1000)  # Adjust the frequency and duration as desired

class PannablePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)

        self.pan_start_pos = None
        self.window_start_pos = None

    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()

    def on_left_down(self, event):
        self.pan_start_pos = event.GetPosition()
        self.window_start_pos = self.GetParent().GetPosition()

    def on_left_up(self, event):
        self.pan_start_pos = None
        self.window_start_pos = None

    def on_motion(self, event):
        if event.Dragging() and event.LeftIsDown() and self.pan_start_pos is not None and self.window_start_pos is not None:
            current_pos = event.GetPosition()
            delta = current_pos - self.pan_start_pos
            new_pos = self.window_start_pos + delta
            self.GetParent().Move(new_pos)

class CountdownFrame(wx.Frame):
    def __init__(self, parent):
        style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.CLOSE_BOX)
        wx.Frame.__init__(self, parent, title="", style=style)
        self.SetBackgroundColour("#7e97ad")
        self.SetSizeHints(360, 100, 360, 100)  # Set fixed size

        # Remove the title bar by hiding the system menu
        self.SetWindowStyleFlag(wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)

        panel = PannablePanel(self)
        panel.SetBackgroundColour("#7e97ad")

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.label = wx.StaticText(panel, label="距离休息还剩 25:00", style=wx.ALIGN_CENTER)
        font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.label.SetFont(font)
        self.label.SetForegroundColour("#edced0")

        sizer.AddStretchSpacer(1)
        sizer.Add(self.label, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.AddStretchSpacer(1)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        restart_button = wx.Button(panel, label="Restart")
        restart_button.Bind(wx.EVT_BUTTON, self.on_restart)
        restart_button.SetBackgroundColour("#7e97ad")
        restart_button.SetForegroundColour("#edced0")

        close_button = wx.Button(panel, label="Close")
        close_button.Bind(wx.EVT_BUTTON, self.on_close)
        close_button.SetBackgroundColour("#7e97ad")
        close_button.SetForegroundColour("#edced0")

        button_sizer.Add(restart_button, 0, wx.ALL, 5)
        button_sizer.AddSpacer(10)
        button_sizer.Add(close_button, 0, wx.ALL, 5)

        sizer.Add(button_sizer, 0, wx.CENTER | wx.BOTTOM, 10)

        panel.SetSizerAndFit(sizer)
        min_width, min_height = sizer.GetMinSize()
        scale_factor = 1.2  # Enlarge the window by 20%
        self.SetSize(int(min_width * scale_factor), int(min_height * scale_factor))

        self.countdown_duration = 25 * 60
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)

        self.restart()

    def restart(self):
        self.start_time = time.time()
        self.end_time = self.start_time + self.countdown_duration
        self.timer.Start(1000)

    def on_timer(self, event):
        current_time = time.time()
        time_left = self.end_time - current_time
        if time_left > 0:
            minutes = int(time_left / 60)
            seconds = int(time_left % 60)
            time_str = f"{minutes:02d}:{seconds:02d}"
            self.label.SetLabel(f"距离休息还剩 {time_str}")
        else:
            self.label.SetLabel("Time's up!")
            self.timer.Stop()
            play_sound()

    def on_restart(self, event):
        if wx.MessageBox("Are you sure you want to restart the countdown?", "Confirmation", wx.YES_NO) == wx.YES:
            self.restart()

    def on_close(self, event):
        if wx.MessageBox("Are you sure you want to close the application?", "Confirmation", wx.YES_NO) == wx.YES:
            self.Close()

if __name__ == '__main__':
    app = wx.App()
    frame = CountdownFrame(None)
    frame.Show()
    app.MainLoop()

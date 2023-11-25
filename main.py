import wx
import wikipedia
import wolframalpha
from espeak import espeak

# Add your Wolfram Alpha App ID here
app_id = "YOUR APP ID"
client = wolframalpha.Client(app_id)

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
                          pos=wx.DefaultPosition, size=wx.Size(450, 100),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                          wx.CLOSE_BOX | wx.CLIP_CHILDREN,
                          title="PyDa")
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel,
                            label="Hello, I am Pyda, the Python Digital Assistant. How can I help you?")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER, size=(400, 30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()

    def OnEnter(self, event):
        input_text = self.txt.GetValue()
        input_text = input_text.lower()

        try:
            res = client.query(input_text)
            answer = next(res.results).text
            print(answer)
            espeak.synth("The answer is " + str(answer))
        except StopIteration:
            print("No results from Wolfram Alpha")
        except Exception as e:
            try:
                input_text = input_text.split(' ')
                input_text = ' '.join(input_text[2:])
                summary = wikipedia.summary(input_text)
                print(summary)
            except wikipedia.exceptions.PageError:
                print("Page not found on Wikipedia")
            except wikipedia.exceptions.DisambiguationError as e:
                print("Disambiguation error: ", e.options)
            except Exception as e:
                print("An error occurred: ", str(e))

if __name__ == "__main__":
    app = wx.App(True)
    frame = MyFrame()
    app.MainLoop()

import matplotlib
matplotlib.use('TKAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as pltlib
import Tkinter
from Tkinter import *
import numpy as np
from serial.tools import list_ports
import serial
import time
waitingTime = 0.1
connectionTimeOut = 3000

logoData ="""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"""


class App_Window(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def waitResponse(self):
        cmd = ""
        x=0
        while(cmd == ""):
            if((x*waitingTime)>connectionTimeOut):
                break
            x = x+1
            cmd = self.ser.read(self.ser.inWaiting()).replace("\n","").replace("\r","")
            time.sleep(waitingTime)
        return cmd
    def waitResponseWithCommand(self,command):
        cmd = ""
        x=0
        while(cmd == ""):
            time.sleep(0.1)
            self.ser.write(command.encode())
            time.sleep(0.1)
            if((x*waitingTime)>connectionTimeOut):
                break
            x = x+1
            cmd = self.ser.read(self.ser.inWaiting()).replace("\n","").replace("\r","")
            print(cmd)
            time.sleep(waitingTime)
        return cmd

    def waitCommand(self,wantedCMD):
        if(self.waitResponse() != wantedCMD):
            return False
        return True

    def waitCommandWithCommand(self,cmd,wantedCMD):
        if(self.waitResponseWithCommand(cmd) != wantedCMD):
            return False
        return True



    def connect(self):
        self.connectBtn['state'] = DISABLED
        self.ser = serial.Serial("/dev/cu.usbmodem1461")
        print("Connecting...")
        self.ser.write(b's')
        ## wait for welcome msg
        if(self.waitCommand("WELCOME")):
            print("welcome msg has been get")
        else:
            self.connectBtn['state'] = "normal"

        ## check double
        self.ser.write(b'REURDY')

        if(self.waitCommand("YES")):
            print("that is ready")
            self.startBtn['state'] = 'normal'
            self.disconnectBtn['state'] = "normal"
            return True
        else:
            print("no that is not ready.")
            self.connectBtn['state'] = "normal"
            return False






    def disconnect(self):
        ## check double
        self.startBtn['state'] = DISABLED
        self.connectBtn['state'] = "normal"
        self.disconnectBtn['state'] = DISABLED
        print("I get data.")
        self.ser.close()


    def start(self):
        ## check double
        self.startBtn['state'] = DISABLED
        self.ser.write(b'IGNPRCDR')
        print("IGNITON!!!")
        time.sleep(0.5);
        if(self.waitCommandWithCommand("REURDY","YES")):
            f = open('tmpdata.txt', 'w')
            time.sleep(0.5)
            self.ser.write(b'DATAPLS')
            f.write(self.waitResponse());
            self.startBtn['state'] = 'normal'
            f.close()
            self.loadLastData()
            return True
        else:
            print("no that is not ready.")
            self.startBtn['state'] = "normal"
            return False






        ##DATAPLS

    def quit(self):
        self.root.destroy()
        self.root.quit()
    def initialize(self):
        self.header = Frame(height=2, bd=1, relief=SUNKEN, bg="#f1f1f1")
        self.header.pack(fill=X, padx=0, pady=0, side=TOP)

        IMAGE_DATA = '''
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
'''

        image = PhotoImage(data=IMAGE_DATA)
        label = Label(self.header, width=250, image=image, padx=20, pady=20, bg="#f1f1f1")
        label.image=image
        label.pack(side=RIGHT,padx=10, pady=10)



        self.controls = Frame(height=2, bd=1, relief=SUNKEN)
        self.controls.pack(fill=Y, padx=5, pady=15, side=LEFT)


        #self.label = Label(self.controls, text="Controls")
        #self.label.pack(padx=10,pady=10)


        self.connectBtn = Tkinter.Button(self.controls,text="Connect",command=self.connect,width=10)
        self.connectBtn.pack(padx=10,pady=10)


        self.disconnectBtn = Tkinter.Button(self.controls,text="Disconnect", state=DISABLED,command=self.disconnect,width=10)
        self.disconnectBtn.pack()


        self.startBtn = Tkinter.Button(self.controls,text="Start",state=DISABLED,command=self.start,width=10)
        self.startBtn.pack()



        ##button = Tkinter.Button(self,text="Open File",command=self.OnButtonClick).pack(side=Tkinter.TOP)
        self.canvasFig=pltlib.figure(1)
        Fig = matplotlib.figure.Figure(figsize=(10,5),dpi=100)
        self.FigSubPlot = Fig.add_subplot(1,1,1)
        self.FigSubPlot.relim()
        self.FigSubPlot.xlim = [0,5000]
        self.FigSubPlot.ylim = [0,5000]
        self.FigSubPlot.autoscale_view(True,True,True)
        self.FigSubPlot.autoscale(True)
        self.line1, = self.FigSubPlot.plot([],[])
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(Fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
        self.canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
        self.update()
    def refreshFigure(self,x,y):
        self.FigSubPlot.plot(x,y)
        self.canvas.draw()
    def loadLastData(self):
        x=[]
        y=[]

        with open("tmpdata.txt") as f:
            for line in f:
                tmp = line.replace("\n","").replace("\r","").split(",")
                if(len(tmp)<2):
                    continue
                ms = tmp[0];
                force = tmp[1].replace(";","")
                x.append(ms)
                y.append(force)
                print(ms+"->("+force+")")
        f.closed
        print(x)
        print(y)
        self.refreshFigure(x,y)


if __name__ == "__main__":
    MainWindow = App_Window(None)
    MainWindow.bind('<Control-c>', quit)
    MainWindow.mainloop()










"""""from Tkinter import *
import ttk
import tkMessageBox
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go


def sayhi(param):
    tkMessageBox.showinfo( "Hello Python", "Hello World")



class App:
    def __init__(self, master):

        headerPack = Frame(master)
        Button(headerPack, text='Top').pack(side=LEFT, anchor=W, fill=X, expand=YES)
        Button(headerPack, text='Center').pack(side=LEFT, anchor=W, fill=X, expand=YES)
        Button(headerPack, text='Bottom').pack(side=LEFT, anchor=W, fill=X, expand=YES)
        headerPack.pack(side=TOP, fill=BOTH)


        content = Frame(master)

        ##  control bar
        controls = Frame(content)
        ttk.Button(controls, text='EKSILT').pack(side=TOP, anchor=W, fill=X, expand=YES)
        ttk.Button(controls, text='Center').pack(side=TOP, anchor=W, fill=X, expand=YES)
        ttk.Button(controls, text='Bottom').pack(side=TOP, anchor=W, fill=X, expand=YES)
        controls.pack(side=RIGHT, fill=Y)


        ##  menu bar
        menu = Frame(content)
        Button(menu, text='Top').pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(menu, text='Center').pack(side=TOP, anchor=W, fill=X, expand=YES)
        Button(menu, text='Bottom').pack(side=TOP, anchor=W, fill=X, expand=YES)
        menu.pack(side=RIGHT, fill=Y)


        ##  order list bar
        order = Frame(content)
        orders = Listbox(order)
        orders.pack(side=TOP, fill=BOTH, expand=YES)
        orders.insert(1, "Python")
        orders.insert(2, "Perl")
        orders.insert(3, "C")
        orders.insert(4, "PHP")
        orders.insert(5, "JSP")
        orders.insert(6, "Ruby")
        order.pack(side=RIGHT, fill=BOTH, expand=YES)


        content.pack(side=TOP, fill=BOTH, expand=YES)




        fm2 = Frame(master)
        Button(fm2, text='Left').pack(side=LEFT)
        Button(fm2, text='This is the Center button').pack(side=LEFT)
        Button(fm2, text='Right').pack(side=LEFT)
        fm2.pack(side=LEFT, padx=10)

root = Tk()
#style = ttk.Style()
#style.configure("Button", foreground="#526271", background="#526271")




N = 500
random_x = np.linspace(0, 1, N)
random_y = np.random.randn(N)

# Create a trace
trace = go.Scatter(
    x = random_x,
    y = random_y
)

data = [trace]

py.iplot(data, filename='basic-line')







root.option_add('*font', ('verdana', 12, 'bold'))
root.title("Pack - Example 13")
display = App(root)
root.mainloop()
"""

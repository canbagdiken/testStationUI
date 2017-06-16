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
        self.controls = Frame(height=2, bd=1, relief=SUNKEN)
        self.controls.pack(fill=Y, padx=5, pady=15, side=LEFT)

        self.connectBtn = Tkinter.Button(self.controls,text="Connect",command=self.connect,width=10)
        self.connectBtn.pack()


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

"""
Lab Practice #1:
“Effect of temperature and Photogenerated Current in a solar cell”
----------------------------------------------
This class computes graphs for different equations related to solar cells

**authors**: Paola Castro *University of Francisco de Paula Santander*
             Sebastian Rojas *University of Francisco de Paula Santander*

..note::
    This class makes inherits from `tkinter`, from `PIL`, from `matplotlib` and from `numpy`
    Check the corresponding documentation below
    <https://docs.python.org/3/library/tk.html>
    <https://pillow.readthedocs.io/en/stable/>
    <https://matplotlib.org/stable/index.html>
    <https://numpy.org/doc/>
"""

from tkinter import *
from PIL import ImageTk, Image #Used to implement images in Tkinter
import matplotlib.pyplot as plt #Used to graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #Connection between Tkinter and matplotlib
import numpy as np #Used to calculate

def root():
    global mainScreen
    mainScreen = Tk()
    mainScreen.title("Práctica de Laboratorio #1")
    mainScreen.geometry("350x450")
    mainScreen.resizable(False,False)
    mainScreen.iconbitmap("Images/Icon.ico")
    #Background mainScreen Image
    mainScreenImage = ImageTk.PhotoImage(Image.open("Images/mainScreen.jpg"))
    Label(image = mainScreenImage).place(x=0,y=0)
    #Functions Images
    firstFunction = ImageTk.PhotoImage(Image.open("Images/firstFunction.png"))
    Label(image = firstFunction).place(x=25,y=160)
    secondFunction = ImageTk.PhotoImage(Image.open("Images/secondFunction.png"))
    Label(image = secondFunction).place(x=25,y=240)
    #Button
    Button(text="INICIAR",height=1,width=10,cursor="hand2",command=graphScreen).place(x=130,y=325)
    #The loop where the app starts
    mainScreen.mainloop()

#----------------------Values----------------------
v = np.arange(0,2.2,0.01) #Defined by the user (V)
k = 1.380649*(10**(-23)) #Boltzmann value (J/K)
Eg = 1.7944*(10**(-19)) #Silicon energy band gap (J)
q = 1.6*(10**(-19)) #Charge of the electron (C)
#n is the ideality factor
#--------------------------------------------------

def graphScreen():
    #This screen appears if the user choose the first function
    mainScreen.destroy()
    global graphScreen
    graphScreen = Tk()
    graphScreen.title("Práctica de Laboratorio #1 - Efecto de la temperatura y la corriente fotogenerada en una celda solar")
    graphScreen.geometry("960x560")
    graphScreen.resizable(False,False)
    graphScreen.iconbitmap("Images/Icon.ico")
    
    #Sliders
    global n, t, il, ioo
    
    Label(text="Factor de idealidad").place(x=40,y=420)
    n = Scale(graphScreen,from_= 1, to = 2, length= 200, resolution=0.01, orient = HORIZONTAL)
    n.place(x=40,y=440)
    
    Label(text="Temperatura (°C)").place(x=270,y=420)
    t = Scale(graphScreen,from_= -15, to = 50, length= 200, orient = HORIZONTAL)
    t.place(x=270,y=440)
    
    Label(text="Corriente IL (A)").place(x=500,y=420)
    il = Scale(graphScreen,from_= 0, to = 8, length= 200, resolution=0.01, orient = HORIZONTAL)
    il.place(x=500,y=440)
    
    Label(text="Corriente Ioo (A/m^2)").place(x=730,y=420)
    ioo = Scale(graphScreen,from_= 10**5, to = 10**-5, length= 200, orient = HORIZONTAL)
    ioo.place(x=730,y=440)
    
    #Figure current vs voltage
    global ax, canvas
    fig, ax = plt.subplots(figsize=(5,4),facecolor='#f0f0f0f0')
    ax.set_title(label="Curva característica de corriente vs voltaje")
    ax.axhline(linewidth=2,color='black')
    ax.axvline(linewidth=2,color='black')
    ax.set_ylim(bottom=0,top=10)
    ax.set_xlim(left=0,right=2.2)
    ax.set_xlabel("Voltaje (V)", color='black')
    ax.set_ylabel("Corriente (A)", color='black')
    
    canvas = FigureCanvasTkAgg(fig, master = graphScreen)
    
    #Figure power vs voltage
    global ax2, canvas2
    fig2, ax2 = plt.subplots(figsize=(5,4),facecolor='#f0f0f0f0')
    ax2.set_title(label="Curva característica de potencia vs voltaje")
    ax2.axhline(linewidth=2,color='black')
    ax2.axvline(linewidth=2,color='black')
    ax2.set_ylim(bottom=0,top=15)
    ax2.set_xlim(left=0,right=2.2)
    ax2.set_xlabel("Voltaje (V)", color='black')
    ax2.set_ylabel("Potencia (W)", color='black')
    
    canvas2 = FigureCanvasTkAgg(fig2, master = graphScreen)
    
    #Labels for some variables
    global label_voc, label_isc, label_vmp, label_imp, label_ff, label_pmax
    Label(text="Voltaje circuito abierto (Voc)",bg="white").place(x=40,y=500)
    Label(text="Corriente corto circuito (Isc)",bg="white").place(x=240,y=500)
    Label(text="Voltaje máxima potencia (Vmp)",bg="white").place(x=440,y=500)
    Label(text="Corriente máxima potencia (Imp)",bg="white").place(x=640,y=500)
    Label(text="Fill Factor (FF)",bg="white").place(x=850,y=500)
    
    label_voc = Label(bg="white")
    label_voc.place(x=40,y=520)
    label_isc = Label(bg="white")
    label_isc.place(x=240,y=520)
    label_vmp = Label(bg="white")
    label_vmp.place(x=440,y=520)
    label_imp = Label(bg="white")
    label_imp.place(x=640,y=520)
    label_ff = Label(bg="white")
    label_ff.place(x=850,y=520)
    label_pmax = Label(bg="white")
    label_pmax.place(x=840,y=60)
    
    #Function that creates every point in the graph
    graphBoth()
    
    #The loop of the screen
    graphScreen.mainloop()

def graphBoth():
    n_var = n.get()
    t_var = t.get()
    t_var = t_var + 273.15 #Convert from Celsius to Kelvin
    il_var = il.get()
    ioo_var = ioo.get()
    
    #Here we calculate the main equations
    io = ioo_var*np.exp(-(Eg/(k*t_var)))
    equation_i = il_var - (io*(np.exp((q*v)/(n_var*k*t_var))-1))
    
    #We create the main variables used in the next steps
    pmax = 0
    vmp = 0
    voc = 0
    imp = 0
    
    #This for tracks the highest value of power (pmax) and saves its
    #position at the voltage value (vmp), with those two parameters
    #it is possible to find the imp, because imp = pmax/vmp
    
    for i in range(0,len(v)-1):
        temp = v[i]*(il_var - (io*(np.exp((q*v[i])/(n_var*k*t_var))-1)))
        if temp > pmax:
            pmax = temp
            vmp = v[i]
            imp = pmax/vmp
    
    #This for looks for the open circuit voltage, it simply checks where
    #the main equation reaches a value below zero, and then saves its position
    #at the voltage axis, so it finds voc
    
    temp3 = 0
    for i in range(0,len(v)-1):
        temp2 = il_var - (io*(np.exp((q*v[i])/(n_var*k*t_var))-1))
        if temp2 < temp3:
            temp3 = temp2
            if temp3 < 0:
                voc = v[i]
                break
    
    #To find the fill factor we use the main equation given by the teacher
    
    ff = (pmax / ((voc*il_var)+0.00001))*100
    
    if ff > 100:
        label_voc.config(text="Fuera de límite")
        label_isc.config(text="Fuera de límite")
        label_vmp.config(text="Fuera de límite")
        label_imp.config(text="Fuera de límite")
        label_ff.config(text="Fuera de límite")
    else:
        label_voc.config(text="{0:.2f}".format(voc) + " V")
        label_isc.config(text="{0:.2f}".format(il_var) + " A")
        label_vmp.config(text="{0:.2f}".format(vmp) + " V")
        label_imp.config(text="{0:.2f}".format(imp) + " A")
        label_ff.config(text="{0:.2f}".format(ff) + " %")
        label_pmax.config(text="Pmax: " + "{0:.2f}".format(pmax) + " W")
    
    line, = ax.plot(v,equation_i,color='b',linestyle='solid')
    linem, = ax.plot(vmp,imp,marker="o",markersize=7,markerfacecolor="red",markeredgecolor="red")
    lineh, = ax.plot([0,vmp],[imp,imp],linestyle='dashed',color='red')
    linev, = ax.plot([vmp,vmp],[0,imp],linestyle='dashed',color='red')
    lineffm, = ax.plot(voc,il_var,marker="o",markersize=7,markerfacecolor="black",markeredgecolor="black")
    lineffh, = ax.plot([0,voc],[il_var,il_var],linestyle='dashed',color='black')
    lineffv, = ax.plot([voc,voc],[0,il_var],linestyle='dashed',color='black')

    line2, = ax2.plot(v,v*equation_i,color='b',linestyle='solid')
    lineh2, = ax2.plot([0,vmp],[pmax,pmax],linestyle='dashed',color='red')
    linev2, = ax2.plot([vmp,vmp],[0,pmax],linestyle='dashed',color='red')
    linem2, = ax2.plot(vmp,pmax,marker="o",markersize=7,markerfacecolor="red",markeredgecolor="red")
    
    
    canvas.get_tk_widget().place(x=0,y=0)
    canvas.draw()
    canvas2.get_tk_widget().place(x=480,y=0)
    canvas2.draw()
    
    #Those lines of code are used to clear the graphs and refresh it
    
    line.set_ydata(v+2**1000)
    linem.set_ydata(v+2**1000)
    lineh.set_ydata(2**1000)
    linev.set_ydata(2**1000)
    lineffm.set_ydata(v+2**1000)
    lineffh.set_ydata(2**1000)
    lineffv.set_ydata(2**1000)
    
    line2.set_ydata(v+2**1000)
    linem2.set_ydata(v+2**1000)
    lineh2.set_ydata(2**1000)
    linev2.set_ydata(2**1000)
    
    graphScreen.after(100,graphBoth)

#This function calls the main app
root()
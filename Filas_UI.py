# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure

class App(tk.Tk):
    
    def __init__(self):
        #Declaracion de la ventana principal y el tamaño de esta
        super().__init__()
        self.geometry("700x500")
        self.title('MODELOS DE FILAS DE ESPERA')
        self.descripciones=['Inserte texto de Ro', 
                            'Inserte texto de Cn',
                            'Probabiliidad 0', 
                            'Probabilidad enesima',
                            'Numero promedio de clientes en la cola',
                            'Numero promedio de clientes en el sistema',
                            'Tiempo esperado en la cola',
                            'Tiempo promeido en el sistema']
        self.arreglo_titulo=['p', 'Cn', 'P0', 'Pn', 'Lq', 'L', 'Wq', 'W']
        # Inicialización del menu principal
        self.menu = ("Modelo M/M/1",
      "Modelo M/M/s",
      "Modelo M/M/s/K",
      "Modelo M/G/1")

        # Variables para manjear las opciones del menu en caso de comprobaciones
        self.option = tk.StringVar(self)
        
        # create widget
        self.create_wigets()
        
    def create_wigets(self):
        # Paddings genéricos
        paddings = {'padx': 5, 'pady': 5}

        # Titulo de la ventana principal
        label = ttk.Label(self,  text='MODELOS DE FILAS DE ESPERA',font = ("Castellar",15))
        label.grid(column=0, row=0, sticky=tk.W, **paddings)

        # Marco donde delimitamos los inputs de los diferentes métodos y declaración del mensaje de error
        self.frame = tk.LabelFrame(self,text="m_m_1_frame", borderwidth=8,  labelanchor = "nw", font = ("Castellar",12))
        self.frame.grid(column=0, row=1,pady=20,padx=10,rowspan=4)
        self.errorText= tk.StringVar()
        self.errorText.set(" ")
        self.errorMessage= tk.Label(self.frame,  textvariable=self.errorText ,font = ("Castellar",8),fg="red")

        self.clearBtn = tk.Button(self, text="Limpiar Historico",font = ("Castellar",8),fg="red")
        
        self.showBtn = tk.Button(self, text="Mostrar Historico",font = ("Castellar",8))

        # option menu
        option_menu = tk.OptionMenu(
            self,
            self.option,
            *self.menu,
            command=self.option_changed)
        
        helv36 = tkFont.Font(family='Castellar', size=8)
        option_menu.config(font=helv36)
        option_menu.grid(column=1, row=0, sticky='e', **paddings,columnspan=2)
        
    def clearData(self,path_to_csv):
        print(path_to_csv)
 
    def showGraph(self,path_to_csv):
        grafica_frame = tk.Toplevel()
        grafica_frame.title("Grafica Historica")
        f = Figure(figsize=(5,5),dpi=100)
        a=f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8], [2,3,5,2,7,8,5,9])
        
        canvas = FigureCanvasTkAgg(f,master=grafica_frame)
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        
        toolbar= NavigationToolbar2Tk(canvas,grafica_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        
        
        print(path_to_csv)
 
    def addToCsv(self,path_to_csv):
        print(path_to_csv)
    
    def creacionTabla(self,arreglo,frame_result,tiempo,path_to_csv):
        helv36 = tkFont.Font(family='Helvetica',
        size=11, weight='bold')
        for i in range(8):
            for j in range(2):
                if j == 0:
                    e = tk.Entry(frame_result,
                                 relief='solid',
                                 borderwidth =2, 
                                 justify=tk.CENTER,
                                 foreground="White",
                                 readonlybackground="Green",
                                 font=helv36)
                
                    e.configure({"background": "Green"})
                else:
                    e = tk.Entry(frame_result,relief='groove',borderwidth =3, justify=tk.CENTER)
                    
                e.grid(row=i+1, column=j, sticky='NSEW')
                e.insert(tk.END, '%s' % (arreglo[j][i]))
                e['state']='readonly'
        
        for i in range(8):
            if(i>=6):
                label1=tk.Label(frame_result,text=self.arreglo_titulo[i]+" : "+self.descripciones[i] + f" ( {tiempo} )",padx=10)
            else:
                label1=tk.Label(frame_result,text=self.arreglo_titulo[i]+" : "+self.descripciones[i],padx=10)
            label1.grid(column=3,row=i+1, sticky='w')
        addBtn = tk.Button(frame_result, 
                           text="Añadir a Historico", 
                           font = ("Castellar",8),
                           fg="green", 
                           command=lambda: self.addToCsv(path_to_csv))
        addBtn.grid(column=0,row=10,columnspan=5,pady=10)
        
    
    def factorial(self,numero):
        factorial = 1
        for i in range(1, numero + 1):
            factorial = factorial * i
        return factorial
        
    def comprobacion_Modelo_M_M_1(self,lamda, mu, n):
        if(lamda < 0 or mu < 0):
            self.errorText.set("El sistema NO puede aceptar valores Negativos")
            self.errorMessage.grid(column=0,row=0,columnspan=2)
            return False  
        if(lamda > mu or lamda == mu):
            self.errorText.set("El sistema siendo planeteado NO es estable. Lambda debe ser menor a mu")
            self.errorMessage.grid(column=0,row=0,columnspan=2)
            return False
        if(n < 0):
            self.errorText.set("El valor de n es menor a 0. NO es aceptable")
            self.errorMessage.grid(column=0,row=0,columnspan=2)
            return False;
        if(n % 1 != 0):
            self.errorText.set("El valor de n NO puede ser decimal")
            self.errorMessage.grid(column=0,row=0,columnspan=2)
            return False; 
        return True
    
    def modelo_M_M_1(self,lamda, mu, tiempo,n):
        p = round((lamda / mu), 4)
        Cn = round((pow(p, n)),4)
        pCero = round((1 - p), 4)
        pN = round((pCero * pow(p, n)), 4)
        Lq = round((pow(lamda, 2) / (mu * (mu - lamda))), 4)
        L = round((lamda / (mu - lamda)), 4)
        Wq = round((lamda /(mu * (mu - lamda))), 4)
        W = round((1 / (mu - lamda)), 4)
        print("p: "+ str(p))
        print("Cn: " + str(Cn))
        print("P0: "+ str(pCero))
        print("Pn: "+ str(pN) + ". Donde n = "+ str(n))
        print("Número promedio de clientes en la cola (Lq): "+ str(Lq) + " clientes") 
        print("Número promedio de clientes en el sistema (L): "+ str(L) + " clientes")
        print("Tiempo esperado en la cola (Wq): "+ str(Wq) + " " + tiempo)
        print("Tiempo promeido en el sistema (W): "+ str(W) + " " + tiempo)
        arreglo_valores_UI = [p, Cn, pCero, pN, Lq, L, Wq, W]
        
        arreglo_tabla=[self.arreglo_titulo,arreglo_valores_UI]

        results = tk.Toplevel()
        results.title("Resultados")
 
        
        result_title=tk.Label(results,text='Resultados del Modelo M/M/1 :',font = ("Castellar",10)).grid(column=0,row=0,padx=7,pady=15,sticky="ew",columnspan=4)
            
        self.creacionTabla(arreglo_tabla,results,tiempo,"m/m/1")
        
            
    def comprobacion_Modelo_M_M_s(self,lamda, mu, s, n):
        if(lamda < 0 or mu < 0):
            self.errorText.set("El sistema NO puede aceptar valores Negativos")
            self.errorMessage.grid(column=0,row=0,columnspan=2)
            return False  
        """if(lamda > mu or lamda == mu):
            print("El sistema siendo planeteado NO es estable. Lambda debe ser menor a mu")
            return False"""
        if(mu * s < lamda):
            self.errorText.set("El sistema siendo planeteado NO es estable. Lambda debe ser menor a mu")
            self.errorMessage.grid(column=0,row=0,columnspan=2)
            return False
        if(n < 0):
            self.errorText.set("El valor de n es menor a 0. NO es aceptable")
            self.errorMessage.grid(column=0,row=0,columnspan=2)
            return False;
        if(n % 1 != 0):
            self.errorText.set("El valor de n NO puede ser decimal")
            self.errorMessage.grid(column=0,row=0,columnspan=2)
            return False; 
        if(s < 0):
            self.errorText.set("El valor de s es menor a 0. NO es aceptable")
            self.errorMessage.grid(column=0,row=0,columnspan=2)
            return False;
        if(s % 1 != 0):
            self.errorText.set("El valor de s NO puede ser decimal")
            self.errorMessage.grid(column=0,row=0,columnspan=2)
            return False; 
        return True
    
    def modelo_M_M_s(self,lamda, mu, tiempo, s, n):

        p = lamda / (s * mu)
        if n >= (s - 1):
            Cn = round((pow(lamda/mu, n) / self.factorial(n)),4)
        else:
            Cn = round((pow(lamda/mu, n) / (self.factorial(s) * pow(s, (n-s)))), 4)
        primerTerminoPCero = 0
        for index in range (0, s): #el ciclo solo hace hasta s - 1
            primerTerminoPCero += (pow(lamda/mu, index) / self.factorial(index))
        pCero = round((1 / (primerTerminoPCero + (pow(lamda/mu, s) / self.factorial(s)) * (1 / (1 - (lamda / (s * mu)))))), 4)
        if n >= 0 and n < s:
            pN = round((((pow(lamda/mu,n)) / self.factorial(n)) * pCero), 4)
        else:
            pN = round((((pow(lamda/mu,n)) / (self.factorial(s) * pow(s, n-s))) * pCero), 4)
        Lq = round(((pCero * pow(lamda / mu, s) * p) / (self.factorial(s) * pow((1 - p), 2))), 4)
        L = round((Lq + (lamda / mu)), 4)
        Wq = round((Lq / lamda), 4)
        W = round((Wq + (1/mu)), 4)
        print("p: "+ str(p))
        print("Cn: " + str(Cn) + ". Donde n = "+ str(n) + " y s = " + str(s))
        print("P0: " + str(pCero) + ". Donde n = "+ str(n) + " y s = " + str(s))
        print("Pn: "+ str(pN) + ". Donde n = "+ str(n) + " y s = " + str(s))
        print("Número promedio de clientes en la cola (Lq): "+ str(Lq) + " clientes")
        print("Número promedio de clientes en el sistema (L): "+ str(L) + " clientes")
        print("Tiempo esperado en la cola (Wq): "+ str(Wq) + " " + tiempo)
        print("Tiempo promeido en el sistema (W): "+ str(W) + " " + tiempo)
        arreglo_valores_UI = [p, Cn, pCero, pN, Lq, L, Wq, W]
        
        
        arreglo_tabla=[self.arreglo_titulo,arreglo_valores_UI]

        results = tk.Toplevel()
        results.title("Resultados")
        rows = []
        result_title=tk.Label(results,text='Resultados del Modelo M/M/S :',font = ("Castellar",10)).grid(column=0,row=0,padx=7,pady=15,sticky="ew",columnspan=4)
        self.creacionTabla(arreglo_tabla,results,tiempo,"M/M/S")

    def m_m_1_frame(self, *args):
        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text']="m_m_1_frame"
        self.setHistoricoBtns("m_m_1_frame")
        
        for widget in self.frame.winfo_children():
            widget.destroy()
            
        # Display de los inputs necesarios para el método
        lambda_label= ttk.Label(self.frame,  text='Tasa de llegadas (lambda) :',font = ("Castellar",8)).grid(column=0,row=1,padx=10,pady=20,sticky="e")
        lambda_input = tk.Entry(self.frame, width=20)
        lambda_input.grid(column=1,row=1,padx=40)
        
        mu_label= ttk.Label(self.frame,  text='Tasa de Servicio (mu) :',font = ("Castellar",8)).grid(column=0,row=2,padx=10,pady=20,sticky="e")
        mu_input = tk.Entry(self.frame, width=20)
        mu_input.grid(column=1,row=2,padx=10)
        
        tiempo_label= ttk.Label(self.frame,  text='Unidad de Tiempo :',font = ("Castellar",8)).grid(column=0,row=3,padx=10,pady=20,sticky="e")
        tiempo_input = tk.Entry(self.frame, width=20)
        tiempo_input.grid(column=1,row=3,padx=10)
        
        n_label= ttk.Label(self.frame,  text='N :',font = ("Castellar",8)).grid(column=0,row=4,padx=10,pady=20,sticky="e")
        n_input = tk.Entry(self.frame, width=20)
        n_input.grid(column=1,row=4,padx=10)
        
        sumbit_btn= tk.Button(self.frame, text="Generar",font = ("Castellar",8), command = lambda: self.aux_m_m_1_frame(lambda_input,mu_input,tiempo_input,n_input))
        sumbit_btn.grid(column=0,row=5, columnspan=3,pady=20)
        
    def aux_m_m_1_frame(self,lambda_input,mu_input,tiempo_input,n_input):
        #Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage= tk.Label(self.frame,  textvariable=self.errorText ,font = ("Castellar",8),fg="red")
        if lambda_input.get() != '' and mu_input.get() != ''and tiempo_input.get() != ''and n_input.get() != '':
            try:    
                x1 = float(lambda_input.get())
                x2 = float(mu_input.get())  
                x4 = float(n_input.get())
            except:
                self.errorText.set('Lambda, mu y n deben ser números')
                self.errorMessage.grid(column=0,row=0,columnspan=2)
                return
            if self.comprobacion_Modelo_M_M_1(x1, x2, x4):
                self.modelo_M_M_1(x1, x2, tiempo_input.get(), x4)
            #self.centrosCuadrados(x1,x2)
        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0,row=0,columnspan=2) 
        
    def m_m_s_frame(self, *args):
        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text']="m_m_s_frame"
        self.setHistoricoBtns("m_m_s_frame")
        
        for widget in self.frame.winfo_children():
            widget.destroy()
            
        # Display de los inputs necesarios para el método
        lambda_label= ttk.Label(self.frame,  text='Tasa de llegadas (lambda) :',font = ("Castellar",8)).grid(column=0,row=1,padx=10,pady=20,sticky="e")
        lambda_input = tk.Entry(self.frame, width=20)
        lambda_input.grid(column=1,row=1,padx=40)
        
        mu_label= ttk.Label(self.frame,  text='Tasa de Servicio (mu) :',font = ("Castellar",8)).grid(column=0,row=2,padx=10,pady=20,sticky="e")
        mu_input = tk.Entry(self.frame, width=20)
        mu_input.grid(column=1,row=2,padx=10)
        
        tiempo_label= ttk.Label(self.frame,  text='Unidad de Tiempo :',font = ("Castellar",8)).grid(column=0,row=3,padx=10,pady=20,sticky="e")
        tiempo_input = tk.Entry(self.frame, width=20)
        tiempo_input.grid(column=1,row=3,padx=10)
        
        server_label= ttk.Label(self.frame,  text='No. de Servidores :',font = ("Castellar",8)).grid(column=0,row=4,padx=10,pady=20,sticky="e")
        server_input = tk.Entry(self.frame, width=20)
        server_input.grid(column=1,row=4,padx=10)
        
        n_label= ttk.Label(self.frame,  text='N :',font = ("Castellar",8)).grid(column=0,row=5,padx=10,pady=20,sticky="e")
        n_input = tk.Entry(self.frame, width=20)
        n_input.grid(column=1,row=5,padx=10)
        
        sumbit_btn= tk.Button(self.frame, text="Generar",font = ("Castellar",8), 
                              command = lambda: self.aux_m_m_s_frame(lambda_input,mu_input,tiempo_input,n_input,server_input))
        
        sumbit_btn.grid(column=0,row=6, columnspan=3,pady=20)
        
    def aux_m_m_s_frame(self,lambda_input,mu_input,tiempo_input,n_input,server_input):
        #Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage= tk.Label(self.frame,  textvariable=self.errorText ,font = ("Castellar",8),fg="red")
        if lambda_input.get() != '' and mu_input.get() != ''and tiempo_input.get() != ''and n_input.get() != '' and server_input.get() != '':
            try:    
                x1 = float(lambda_input.get())
                x2 = float(mu_input.get()) 
                x3 = int(server_input.get()) 
                x4 = int(n_input.get())
            except:
                self.errorText.set('Lambda, mu, n y el no. de servidores deben ser números')
                self.errorMessage.grid(column=0,row=0,columnspan=2)
                return
            if self.comprobacion_Modelo_M_M_s(x1, x2, x3, x4):
                self.modelo_M_M_s(x1, x2, tiempo_input.get(),x3, x4)

        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0,row=0,columnspan=2)       
        
    def m_m_s_K_frame(self, *args):
        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text']="m_m_s_K_frame"
        self.setHistoricoBtns("m_m_s_K_frame")
        
        for widget in self.frame.winfo_children():
            widget.destroy()
            
        # Display de los inputs necesarios para el método
        lambda_label= ttk.Label(self.frame,  text='Tasa de llegadas (lambda) :',font = ("Castellar",8)).grid(column=0,row=1,padx=10,pady=20,sticky="e")
        lambda_input = tk.Entry(self.frame, width=20)
        lambda_input.grid(column=1,row=1,padx=40)
        
        mu_label= ttk.Label(self.frame,  text='Tasa de Servicio (mu) :',font = ("Castellar",8)).grid(column=0,row=2,padx=10,pady=20,sticky="e")
        mu_input = tk.Entry(self.frame, width=20)
        mu_input.grid(column=1,row=2,padx=10)
        
        tiempo_label= ttk.Label(self.frame,  text='Unidad de Tiempo :',font = ("Castellar",8)).grid(column=0,row=3,padx=10,pady=20,sticky="e")
        tiempo_input = tk.Entry(self.frame, width=20)
        tiempo_input.grid(column=1,row=3,padx=10)
        
        server_label= ttk.Label(self.frame,  text='No. de Servidores :',font = ("Castellar",8)).grid(column=0,row=4,padx=10,pady=20,sticky="e")
        server_input = tk.Entry(self.frame, width=20)
        server_input.grid(column=1,row=4,padx=10)
        
        n_label= ttk.Label(self.frame,  text='N :',font = ("Castellar",8)).grid(column=0,row=5,padx=10,pady=20,sticky="e")
        n_input = tk.Entry(self.frame, width=20)
        n_input.grid(column=1,row=5,padx=10)
        
        sumbit_btn= tk.Button(self.frame, text="Generar",font = ("Castellar",8), 
                              command = lambda: self.aux_m_m_s_K_frame(lambda_input,mu_input,tiempo_input,n_input,server_input))
        
        sumbit_btn.grid(column=0,row=6, columnspan=3,pady=20)
        
    def aux_m_m_s_K_frame(self, lambda_input,mu_input,tiempo_input,n_input,server_input):   
        #Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage= tk.Label(self.frame,  textvariable=self.errorText ,font = ("Castellar",8),fg="red")
        if lambda_input.get() != '' and mu_input.get() != ''and tiempo_input.get() != ''and n_input.get() != '' and server_input.get() != '':
            try:    
                x1 = float(lambda_input.get())
                x2 = float(mu_input.get()) 
                x3 = float(server_input.get()) 
                x4 = float(n_input.get())
            except:
                self.errorText.set('Lambda, mu, n y el no. de servidores deben ser números')
                self.errorMessage.grid(column=0,row=0,columnspan=2)
                return
            if True:
                print("M/M/S/K DEBUG")
                #self.modelo_M_M_1(x1, x2, tiempo_input.get(), x4)

        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0,row=0,columnspan=2)  
            
    def m_G_1_frame(self, *args):
        
        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text']="m_G_1_frame"
        self.setHistoricoBtns("m_G_1_frame")
        
        for widget in self.frame.winfo_children():
            widget.destroy()
            
        # Display de los inputs necesarios para el método
        lambda_label= ttk.Label(self.frame,  text='Tasa de llegadas (lambda) :',font = ("Castellar",8)).grid(column=0,row=1,padx=10,pady=20,sticky="e")
        lambda_input = tk.Entry(self.frame, width=20)
        lambda_input.grid(column=1,row=1,padx=40)
        
        mu_label= ttk.Label(self.frame,  text='Tasa de Servicio (mu) :',font = ("Castellar",8)).grid(column=0,row=2,padx=10,pady=20,sticky="e")
        mu_input = tk.Entry(self.frame, width=20)
        mu_input.grid(column=1,row=2,padx=10)
        
        tiempo_label= ttk.Label(self.frame,  text='Unidad de Tiempo :',font = ("Castellar",8)).grid(column=0,row=3,padx=10,pady=20,sticky="e")
        tiempo_input = tk.Entry(self.frame, width=20)
        tiempo_input.grid(column=1,row=3,padx=10)
        
        server_label= ttk.Label(self.frame,  text='No. de Servidores :',font = ("Castellar",8)).grid(column=0,row=4,padx=10,pady=20,sticky="e")
        server_input = tk.Entry(self.frame, width=20)
        server_input.grid(column=1,row=4,padx=10)
        
        n_label= ttk.Label(self.frame,  text='N :',font = ("Castellar",8)).grid(column=0,row=5,padx=10,pady=20,sticky="e")
        n_input = tk.Entry(self.frame, width=20)
        n_input.grid(column=1,row=5,padx=10)
        
        sumbit_btn= tk.Button(self.frame, text="Generar",font = ("Castellar",8), 
                              command = lambda: self.aux_m_G_1_frame(lambda_input,mu_input,tiempo_input,n_input,server_input))
        sumbit_btn.grid(column=0,row=6, columnspan=3,pady=20)
        
    def aux_m_G_1_frame(self, lambda_input,mu_input,tiempo_input,n_input,server_input):   
        #Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage= tk.Label(self.frame,  textvariable=self.errorText ,font = ("Castellar",8),fg="red")
        if lambda_input.get() != '' and mu_input.get() != ''and tiempo_input.get() != ''and n_input.get() != '' and server_input.get() != '':
            try:    
                x1 = float(lambda_input.get())
                x2 = float(mu_input.get()) 
                x3 = float(server_input.get()) 
                x4 = float(n_input.get())
            except:
                self.errorText.set('Lambda, mu, n y el no. de servidores deben ser números')
                self.errorMessage.grid(column=0,row=0,columnspan=2)
                return
            if True:
                print("M/G/1 DEBUG")
                #self.modelo_M_M_1(x1, x2, tiempo_input.get(), x4)

        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0,row=0,columnspan=2)  
        
    def option_changed(self, *args):
        if self.option.get() == self.menu[0]:
            self.m_m_1_frame()
        elif self.option.get() == self.menu[1]:
            self.m_m_s_frame()
        elif self.option.get() == self.menu[2]:
            self.m_m_s_K_frame()
        elif self.option.get() == self.menu[3]:
            self.m_G_1_frame()
            
    def setHistoricoBtns(self,path_to_csv):
        self.clearBtn['command']=lambda: self.clearData(path_to_csv)
        self.showBtn['command']=lambda: self.showGraph(path_to_csv)
        self.clearBtn.grid(column=2,row=1,sticky='n',pady=(30,0))
        self.showBtn.grid(column=2,row=2,sticky='n')

if __name__ == "__main__":
    app = App()
    app.mainloop()
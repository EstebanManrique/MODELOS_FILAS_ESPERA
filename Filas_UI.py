# -*- coding: utf-8 -*-
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib as mpl
from PIL import ImageTk, Image
from io import BytesIO
import os
import csv
import sympy as sp
from matplotlib.mathtext import math_to_image
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont

import matplotlib
matplotlib.use("TkAgg")

mpl.rcParams.update(mpl.rcParamsDefault)


class App(tk.Tk):

    def __init__(self):
        # Declaracion de la ventana principal y el tamaño de esta
        super().__init__()
        self.geometry("700x500")
        self.title('MODELOS DE FILAS DE ESPERA')
        self.descripciones = ['Factor de utilización',
                              'Notación simplificada para estado estable de sistema',
                              'Probabilidad de que primer servidor esté ocupado',
                              'Probabilidad de que el servidor n esté ocupado',
                              'Promedio de clientes en la cola',
                              'Promedio de clientes en el sistema',
                              'Tiempo esperado en la cola',
                              'Tiempo promeido en el sistema',
                              "Tasa efectiva de arribo al sistema"]
        self.arreglo_titulo = ['p', 'Cn', 'P0',
                               'Pn', 'Lq', 'L', 'Wq', 'W', 'lambdaE']
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
        label = ttk.Label(
            self,  text='MODELOS DE FILAS DE ESPERA', font=("Castellar", 15))
        label.grid(column=0, row=0, sticky=tk.W, **paddings)

        # Marco donde delimitamos los inputs de los diferentes métodos y declaración del mensaje de error
        self.frame = tk.LabelFrame(
            self, text="m_m_1_frame", borderwidth=8,  labelanchor="nw", font=("Castellar", 12))
        self.frame.grid(column=0, row=1, pady=20, padx=10, rowspan=4)
        self.errorText = tk.StringVar()
        self.errorText.set(" ")
        self.errorMessage = tk.Label(
            self.frame,  textvariable=self.errorText, font=("Castellar", 8), fg="red")

        self.clearBtn = tk.Button(
            self, text="Limpiar Historico", font=("Castellar", 8), fg="red")

        self.showBtn = tk.Button(
            self, text="Mostrar Historico", font=("Castellar", 8))

        # option menu
        option_menu = tk.OptionMenu(
            self,
            self.option,
            *self.menu,
            command=self.option_changed)

        helv36 = tkFont.Font(family='Castellar', size=8)
        option_menu.config(font=helv36)
        option_menu.grid(column=1, row=0, sticky='e', **paddings, columnspan=2)

    def clearData(self, archivo):
        if os.path.exists(archivo):
            os.remove(archivo)
        else:
            print("El archivo estadistico ya esta reseteado")

    def promedio(self, lista):
        suma = 0
        for element in lista:
            suma += element
        return (suma / len(lista))

    def showGraph(self, archivo):
        grafica_frame = tk.Toplevel()
        grafica_frame.title("Grafica Historica")

        if os.path.exists(archivo):
            with open(archivo, "r", newline="") as file:
                lector = csv.reader(file)
                infoArchivo = []
                for row in lector:
                    infoArchivo.append(row)
            numeroPuntos = int(infoArchivo[0][0])
            indiceHistoricos = []
            for index in range(1, numeroPuntos + 1):
                indiceHistoricos.append(index)
            for index in range(0, numeroPuntos):
                infoArchivo[1][index] = float(infoArchivo[1][index])
            for index in range(0, numeroPuntos):
                infoArchivo[2][index] = float(infoArchivo[2][index])

            promedioCola = self.promedio(infoArchivo[1])
            promedioSistema = self.promedio(infoArchivo[2])
            puntosCola = []
            puntosSistema = []
            for index in range(0, numeroPuntos):
                puntosCola.append(promedioCola)
                puntosSistema.append(promedioSistema)

        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot(indiceHistoricos, infoArchivo[1], label="Tiempo en Cola")
        a.plot(indiceHistoricos, infoArchivo[2], label="Tiempo en Sistema")
        a.plot(indiceHistoricos, puntosCola,
               label="Promedio en Cola (" + str(promedioCola)+")")
        a.plot(indiceHistoricos, puntosSistema,
               label="Promedio en Sistema (" + str(promedioSistema)+")")
        a.set_xticks(
            range(indiceHistoricos[0], indiceHistoricos[len(indiceHistoricos) - 1] + 1))
        a.set_ylabel("Numero de simulacion")
        a.set_xlabel("Unidades de tiempo")
        a.legend()
        canvas = FigureCanvasTkAgg(f, master=grafica_frame)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, grafica_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def escrituraCsv(self, archivo, tiempoCola, tiempoSistema):
        numeroEscenarios = 0
        tiemposColas = []
        tiemposSistema = []
        if os.path.exists(archivo):
            with open(archivo, "r", newline="") as file:
                lector = csv.reader(file)
                index = 0
                for row in lector:
                    if index == 0:
                        numeroEscenarios = row
                        numeroEscenarios = int(numeroEscenarios[0])
                    if index == 1:
                        tiemposColas = row
                    if index == 2:
                        tiemposSistema = row
                    index += 1
            numeroEscenarios += 1
            tiemposSistema.append(str(float(tiempoSistema)))
            tiemposColas.append(str(float(tiempoCola)))
            with open(archivo, "w", newline="") as file:
                escritor = csv.writer(file, delimiter=",")
                escritor.writerow(str(numeroEscenarios))
                escritor.writerow(tiemposColas)
                escritor.writerow(tiemposSistema)
        else:
            with open(archivo, "w", newline="") as file:
                escritor = csv.writer(file, delimiter=",")
                contenido = []
                contenido.extend(
                    [str(1), str(float(tiempoCola)), str((float(tiempoSistema)))])
                for index in contenido:
                    escritor.writerow([index])

    def mm1_iniciacionDeTabla(self, arreglo, frame_result, tiempo, path_to_csv, size):
        helv36 = tkFont.Font(family='Helvetica',
                             size=11, weight='bold')
        for i in range(size):

            l = tk.Label(frame_result,
                         borderwidth=2,
                         justify=tk.CENTER,
                         foreground="White",
                         background="green",
                         text=(arreglo[0][i]))

            l.grid(row=i+1, column=0, sticky='NSEW')

        for i in range(size):
            if(i >= 6):
                label1 = tk.Label(
                    frame_result, text=self.arreglo_titulo[i]+" : "+self.descripciones[i] + f" ( {tiempo} )", padx=10)
            else:
                label1 = tk.Label(
                    frame_result, text=self.arreglo_titulo[i]+" : "+self.descripciones[i], padx=10)
            label1.grid(column=3, row=i+1, sticky='w')
        addBtn = tk.Button(frame_result,
                           text="Añadir a Historico",
                           font=("Castellar", 8),
                           fg="green",
                           command=lambda: self.escrituraCsv(path_to_csv, arreglo[1][6], arreglo[1][7]))
        addBtn.grid(column=0, row=10, columnspan=5, pady=10)

    def mm1_tabla_latex(self, arreglo, frame_result, size):
        buffer = BytesIO()
        buffer2 = BytesIO()
        for i in range(size):

            if i == 1:
                math_to_image(r'${0}^n$'.format(
                    str(arreglo[1][1])), buffer, dpi=100, format='png')
                buffer.seek(0)

                pimage = Image.open(buffer)
                image = ImageTk.PhotoImage(pimage)

                l = tk.Label(frame_result, image=image, text="")
                l.img = image
                l.grid(row=i+1, column=1, sticky='NSEW')
            elif i == 3:
                math_to_image(r'${0}({1}^n)$'.format(str(arreglo[1][2]), str(
                    arreglo[1][0])), buffer2, dpi=100, format='jpg')
                buffer2.seek(0)

                pimage2 = Image.open(buffer2)
                image2 = ImageTk.PhotoImage(pimage2)

                l2 = tk.Label(frame_result, image=image2)
                l2.img = image2
                l2.grid(row=i+1, column=1, sticky='NSEW')
            else:
                l = tk.Label(frame_result, borderwidth=3,
                             justify=tk.CENTER, text=(arreglo[1][i]))
                l.grid(row=i+1, column=1, sticky='NSEW')

        buffer.flush()
        buffer2.flush()

    def mms_iniciacionDeTabla(self, arreglo, frame_result, tiempo, path_to_csv, size):
        helv36 = tkFont.Font(family='Helvetica',
                             size=11, weight='bold')
        x = 0
        for i in range(size):
            if i == 1 or i == 3:
                l = tk.Label(frame_result,
                             borderwidth=2,
                             height=10,
                             width=7,
                             foreground="White",
                             background="green",
                             text=(arreglo[0][i]))
                l.grid(row=x+1, column=0, rowspan=2, padx=5, pady=2)
                x += 2
            else:
                l = tk.Label(frame_result,
                             borderwidth=2,
                             foreground="White",
                             background="green",
                             height=3,
                             width=7,
                             text=(arreglo[0][i]))
                l.grid(row=x+1, column=0, padx=5, pady=2)
                x += 1
        x = 0
        for i in range(size):
            if(i >= 6):
                label1 = tk.Label(
                    frame_result, text=self.arreglo_titulo[i]+" : "+self.descripciones[i] + f" ( {tiempo} )", padx=10)
            else:
                label1 = tk.Label(
                    frame_result, text=self.arreglo_titulo[i]+" : "+self.descripciones[i], padx=10)

            if i == 1 or i == 3:
                label1.grid(column=3, row=x+1, sticky='NSEW')
                x += 2
            else:
                label1.grid(column=3, row=x+1, sticky='w')
                x += 1

        addBtn = tk.Button(frame_result,
                           text="Añadir a Historico",
                           font=("Castellar", 8),
                           fg="green",
                           command=lambda: self.escrituraCsv("modelo_M_M_s.csv", arreglo[1][6], arreglo[1][7]))
        addBtn.grid(column=0, row=12, columnspan=5, pady=10)

    def mms_tabla_latex(self, arreglo, frame_result, size):
        buffer = BytesIO()
        buffer2 = BytesIO()
        buffer3 = BytesIO()
        buffer4 = BytesIO()
        arrayBuffer = [buffer, buffer2, buffer3, buffer4]

        x = 0
        for i in range(size):

            # print(arreglo[1][3][0])
            if i == 1:

                for y in range(2):
                    math_to_image(arreglo[1][1][y],
                                  arrayBuffer[y], dpi=150, format='jpg')
                    arrayBuffer[y].seek(0)
                    pimage = Image.open(arrayBuffer[y])
                    image = ImageTk.PhotoImage(pimage)
                    l = tk.Label(frame_result, image=image, text="")
                    l.img = image
                    l.grid(row=x+1+y, column=1, sticky='NSEW')
                x += 1

            elif i == 3:
                for y in range(2):
                    math_to_image(arreglo[1][3][y],
                                  arrayBuffer[y+2], dpi=150, format='jpg')
                    arrayBuffer[y+2].seek(0)
                    pimage = Image.open(arrayBuffer[y+2])
                    image = ImageTk.PhotoImage(pimage)
                    l = tk.Label(frame_result, image=image, text="")
                    l.img = image
                    l.grid(row=x+1+y, column=1, sticky='NSEW')
                x += 1

            else:
                l = tk.Label(frame_result, borderwidth=3,
                             justify=tk.CENTER, text=(arreglo[1][i]))
                l.grid(row=x+1, column=1, sticky='NSEW')
            x += 1
        buffer.flush()
        buffer2.flush()
        buffer3.flush()
        buffer4.flush()

    def mmsK_iniciacionDeTabla(self, arreglo, frame_result, tiempo, path_to_csv, size):
        helv36 = tkFont.Font(family='Helvetica',
                             size=11, weight='bold')
        x = 0
        for i in range(size):
            if i == 1 or i == 3:
                l = tk.Label(frame_result,
                             borderwidth=2,
                             height=10,
                             width=7,
                             foreground="White",
                             background="green",
                             text=(arreglo[0][i]))
                l.grid(row=x+1, column=0, rowspan=3, padx=5, pady=2)
                x += 3
            else:
                l = tk.Label(frame_result,
                             borderwidth=2,
                             foreground="White",
                             background="green",
                             height=3,
                             width=7,
                             text=(arreglo[0][i]))
                l.grid(row=x+1, column=0, padx=5, pady=2)
                x += 1
        x = 0
        for i in range(size):
            if(i >= 6):
                label1 = tk.Label(
                    frame_result, text=self.arreglo_titulo[i]+" : "+self.descripciones[i] + f" ( {tiempo} )", padx=10)
            else:
                label1 = tk.Label(
                    frame_result, text=self.arreglo_titulo[i]+" : "+self.descripciones[i], padx=10)

            if i == 1 or i == 3:
                label1.grid(column=3, row=x+1, sticky='NSEW')
                x += 3
            else:
                label1.grid(column=3, row=x+1, sticky='w')
                x += 1

        addBtn = tk.Button(frame_result,
                           text="Añadir a Historico",
                           font=("Castellar", 8),
                           fg="green",
                           command=lambda: self.escrituraCsv("modelo_M_M_s_K.csv", arreglo[1][6], arreglo[1][7]))
        addBtn.grid(column=0, row=15, columnspan=5, pady=10)

    def mmsK_tabla_latex(self, arreglo, frame_result, size):
        buffer = BytesIO()
        buffer2 = BytesIO()
        buffer3 = BytesIO()
        buffer4 = BytesIO()
        buffer5 = BytesIO()
        buffer6 = BytesIO()
        arrayBuffer = [buffer, buffer2, buffer3, buffer4, buffer5, buffer6]

        x = 0
        for i in range(size):

            print(arreglo[1][3][2])
            if i == 1:

                for y in range(3):
                    math_to_image(arreglo[1][1][y],
                                  arrayBuffer[y], dpi=150, format='jpg')
                    arrayBuffer[y].seek(0)
                    pimage = Image.open(arrayBuffer[y])
                    image = ImageTk.PhotoImage(pimage)
                    l = tk.Label(frame_result, image=image, text="")
                    l.img = image
                    l.grid(row=x+1+y, column=1, sticky='NSEW')
                x += 2

            elif i == 3:
                for y in range(3):
                    math_to_image(arreglo[1][3][y],
                                  arrayBuffer[y+3], dpi=150, format='jpg')
                    arrayBuffer[y+3].seek(0)
                    pimage = Image.open(arrayBuffer[y+3])
                    image = ImageTk.PhotoImage(pimage)
                    l = tk.Label(frame_result, image=image, text="")
                    l.img = image
                    l.grid(row=x+1+y, column=1, sticky='NSEW')
                x += 2

            else:
                l = tk.Label(frame_result, borderwidth=3,
                             justify=tk.CENTER, text=(arreglo[1][i]))
                l.grid(row=x+1, column=1, sticky='NSEW')
            x += 1
        buffer.flush()
        buffer2.flush()
        buffer3.flush()
        buffer4.flush()

    def factorial(self, numero):
        factorial = 1
        for i in range(1, numero + 1):
            factorial = factorial * i
        return factorial

    def comprobacion_Modelo_M_M_1(self, lamda, mu):
        if(lamda < 0 or mu < 0):
            self.errorText.set("El sistema NO puede aceptar valores Negativos")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(lamda > mu or lamda == mu):
            self.errorText.set(
                "El sistema siendo planeteado NO es estable. Lambda debe ser menor a mu")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        return True

    def modelo_M_M_1(self, lamda, mu, tiempo):
        p = round((lamda / mu), 4)
        Cn = p
        pCero = round((1 - p), 4)
        # round((pCero * pow(p, n)), 4)
        pN = str(pCero) + "(" + str(p) + " ** n)"
        Lq = round((pow(lamda, 2) / (mu * (mu - lamda))), 4)
        L = round((lamda / (mu - lamda)), 4)
        Wq = round((lamda / (mu * (mu - lamda))), 4)
        W = round((1 / (mu - lamda)), 4)
        """
        print("p: "+ str(p))
        print("Cn: " + str(Cn))
        print("P0: "+ str(pCero))
        print("Pn: "+ str(pN))
        print("Número promedio de clientes en la cola (Lq): "+ str(Lq) + " clientes") 
        print("Número promedio de clientes en el sistema (L): "+ str(L) + " clientes")
        print("Tiempo esperado en la cola (Wq): "+ str(Wq) + " " + tiempo)
        print("Tiempo promeido en el sistema (W): "+ str(W) + " " + tiempo)
        """

        arreglo_valores_UI = [p, Cn, pCero, pN, Lq, L, Wq, W]

        arreglo_tabla = [self.arreglo_titulo, arreglo_valores_UI]

        results = tk.Toplevel()
        results.title("Resultados")

        result_title = tk.Label(results, text='Resultados del Modelo M/M/1 :', font=(
            "Castellar", 10)).grid(column=0, row=0, padx=7, pady=15, sticky="ew", columnspan=4)

        # self.creacionTabla(arreglo_tabla,results,tiempo,"m/m/1",8)
        self.mm1_iniciacionDeTabla(
            arreglo_tabla, results, tiempo, "modelo_M_M_1.csv", 8)
        self.mm1_tabla_latex(arreglo_tabla, results, 8)

    def comprobacion_Modelo_M_M_s(self, lamda, mu, s):
        if(lamda < 0 or mu < 0):
            self.errorText.set("El sistema NO puede aceptar valores Negativos")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        """if(lamda > mu or lamda == mu):
            print("El sistema siendo planeteado NO es estable. Lambda debe ser menor a mu")
            return False"""
        if(mu * s < lamda):
            self.errorText.set(
                "El sistema siendo planeteado NO es estable. Lambda debe ser menor a mu")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(s < 0):
            self.errorText.set("El valor de s es menor a 0. NO es aceptable")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(s % 1 != 0):
            self.errorText.set("El valor de s NO puede ser decimal")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        return True

    def modelo_M_M_s(self, lamda, mu, tiempo, s):
        # r'${0}^n$'.format(str(arreglo[1][1]))
        p = round((lamda / (s * mu)), 4)
        temp1 = str(round((lamda/mu), 4))
        temp2 = str(self.factorial(s))
        Cn = []
        #r'$ (\frac{{{0}}} {{n!}})^n \Longrightarrow 0 \leq n < s$.'.format(p)
        Cn1 = r'$ (\frac{{{0}^n}} {{n!}}) \Longrightarrow 0 \leq n < s$.'.format(
            temp1)
        #Cn1 = "(" + str(round((lamda/mu), 4)) + " ** n) / n!"
        Cn2 = r'$ (\frac{{{0}^n}} {{ {1}({2}^ {{n-a}} ) }}) \Longrightarrow n\geq s$.'.format(
            temp1, temp2, s)

        # Cn1 es para casos donde n = 1,2,...,s-1 y Cn2 es para casos donde n = s,s+1,...
        Cn.extend([Cn1, Cn2])
        """if n <= (s - 1):
            Cn = round((pow(lamda/mu, n) / factorial(n)),4)
        else:
            Cn = round((pow(lamda/mu, n) / (factorial(s) * pow(s, (n-s)))), 4)"""
        primerTerminoPCero = 0
        for index in range(0, s):  # el ciclo solo hace hasta s - 1
            primerTerminoPCero += (pow(lamda/mu, index) /
                                   self.factorial(index))
        pCero = round((1 / (primerTerminoPCero + (pow(lamda/mu, s) /
                      self.factorial(s)) * (1 / (1 - (lamda / (s * mu)))))), 4)
        pN = []
        Pn1 = r'$ (\frac{{{0}^n}} {{n!}}){{{1}}} \Longrightarrow 0 \leq n < s$.'.format(
            temp1, pCero)
        #Pn1 = "((" + str(round((lamda/mu), 4)) + " ** n) / n!) * " + str(pCero)
        # Pn2 = "((" + str(round((lamda/mu), 4)) + " ** n) / (" + str(self.factorial(s)
        #                                                           ) + " * (" + str(s) + " ** (n - " + str(s) + ")))) * " + str(pCero)
        Pn2 = r'$ (\frac{{{0}^n}} {{ {1}({2}^ {{n-a}} ) }}){{{3}}} \Longrightarrow n\geq s$.'.format(
            temp1, temp2, s, pCero)
        # Pn1 es para casos donde 0 <= n < s y Pn2 es para casos donde n >= s
        pN.extend([Pn1, Pn2])
        """if n >= 0 and n < s:
            pN = round((((pow(lamda/mu,n)) / factorial(n)) * pCero), 4)
        else:
            pN = round((((pow(lamda/mu,n)) / (factorial(s) * pow(s, n-s))) * pCero), 4)"""
        Lq = round(((pCero * pow(lamda / mu, s) * p) /
                   (self.factorial(s) * pow((1 - p), 2))), 4)
        L = round((Lq + (lamda / mu)), 4)
        Wq = round((Lq / lamda), 4)
        W = round((Wq + (1/mu)), 4)
        print("p: " + str(p))
        #print("Cn: " + str(Cn) + ". Donde n = "+ str(n) + " y s = " + str(s))
        print("Cn1: " + str(Cn1) + " para casos donde n = 1,2,...,s-1")
        print("Cn2: " + str(Cn2) + " para casos donde n = s,s+1,...")
        print("P0: " + str(pCero))
        #print("Pn: "+ str(pN) + ". Donde n = "+ str(n) + " y s = " + str(s))
        print("Pn1: " + str(Pn1) + " para casos donde 0 <= n < s")
        print("Pn2: " + str(Pn2) + " para casos donde n >= s")
        print("Número promedio de clientes en la cola (Lq): " +
              str(Lq) + " clientes")
        print("Número promedio de clientes en el sistema (L): " +
              str(L) + " clientes")
        print("Tiempo esperado en la cola (Wq): " + str(Wq) + " " + tiempo)
        print("Tiempo promeido en el sistema (W): " + str(W) + " " + tiempo)
        arreglo_valores_UI = [p, Cn, pCero, pN, Lq, L, Wq, W]

        arreglo_tabla = [self.arreglo_titulo, arreglo_valores_UI]

        results = tk.Toplevel()
        results.title("Resultados")
        rows = []
        result_title = tk.Label(results, text='Resultados del Modelo M/M/S :', font=(
            "Castellar", 10)).grid(column=0, row=0, padx=7, pady=15, sticky="ew", columnspan=4)
        # self.creacionTabla(arreglo_tabla,results,tiempo,"M/M/S",8)
        self.mms_iniciacionDeTabla(arreglo_tabla, results, tiempo, "m/m/1", 8)
        self.mms_tabla_latex(arreglo_tabla, results, 8)

    def comprobacion_Modelo_M_M_s_K(self, lamda, mu, s, K):
        if(lamda < 0 or mu < 0):
            self.errorText.set("El sistema NO puede aceptar valores Negativos")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(mu * s < lamda):
            self.errorText.set(
                "El sistema siendo planeteado NO es estable. Lambda debe ser menor a mu")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(K < 0):
            self.errorText.set("El valor de K es menor a 0. NO es aceptable")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(K % 1 != 0):
            self.errorText.set("El valor de K NO puede ser decimal")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(s < 0):
            self.errorText.set("El valor de s es menor a 0. NO es aceptable")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(s % 1 != 0):
            self.errorText.set("El valor de s NO puede ser decimal")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        if(s > K):
            self.errorText.set(
                "El valor de K debe ser menor o igual a S para este modelo")
            self.errorMessage.grid(column=0, row=0, columnspan=2)
            return False
        return True

    def modelo_M_M_s_K(self, lamda, mu, tiempo, s, K):
        p = round((lamda / (s * mu)), 4)
        Cn = []
        temp1 = str(round((lamda/mu), 4))
        temp2 = str(self.factorial(s))
        #Cn1 = "(" + str(round((lamda/mu), 4)) + " ** n) / n!"
        Cn1 = r'$ (\frac{{{0}^n}} {{n!}}) \Longrightarrow 0 \leq n < s$.'.format(
            temp1)
        """Cn2 = "(" + str(round((lamda/mu), 4)) + " ** n) / (" + \
            str(self.factorial(s)) + \
            " * (" + str(s) + " ** (n - " + str(s) + ")))
        """
        Cn2 = r'$ (\frac{{{0}^n}} {{ {1}({2}^ {{n-a}} ) }}) \Longrightarrow n\geq s$.'.format(
            temp1, temp2, s)
        Cn3 = r'$ 0 \Longrightarrow n\geq K$.'
        # Cn1 es para casos donde n = 0,1,2,...,s-1,  Cn2 es para casos donde n = s,s+1,...K y Cn3 es para casos donde n > K
        Cn.extend([Cn1, Cn2, Cn3])
        """if n <= (s - 1):
            Cn = round(((pow((lamda / mu), n)) / (factorial(n))), 4)
        elif n == s or n < (s + 1) or n == K:
            Cn = round(((pow((lamda / mu), n)) / (factorial(s) * pow(s, n-s))), 4)
        else:
            Cn = 0"""
        primerTerminoPCero = 0
        for index in range(0, (s+1)):  # el ciclo solo llega a s
            primerTerminoPCero += (pow((lamda / mu), index)
                                   ) / (self.factorial(index))
        tercerTerminoPCero = 0
        for index in range((s+1), (K + 1)):  # el ciclo solo llega a K
            tercerTerminoPCero += pow(lamda / (s * mu), (index - s))
        pCero = round((1 / (primerTerminoPCero + (pow((lamda / mu),
                      s) / self.factorial(s)) * tercerTerminoPCero)), 4)
        pN = []
        #Pn1 = "((" + str(round((lamda/mu), 4)) + " ** n) / n!) * " + str(pCero)
        Pn1 = r'$ (\frac{{{0}^n}} {{n!}}){{{1}}} \Longrightarrow 0 \leq n < s$.'.format(
            temp1, pCero)
        Pn2 = r'$ (\frac{{{0}^n}} {{ {1}({2}^ {{n-a}} ) }}){{{3}}} \Longrightarrow n\geq s$.'.format(
            temp1, temp2, s, pCero)
        # Pn2 = "((" + str(round((lamda/mu), 4)) + " ** n) / (" + str(self.factorial(s)
        # ) + " * (" + str(s) + " ** (n - " + str(s) + ")))) * " + str(pCero)
        Pn3 = r'$ 0 \Longrightarrow n\geq K$.'
        # Pn1 es para casos donde n = 1,2,...,s-1, Pn2 es para casos donde n = s,s+1,...K y Pn3 es para casos donde n > K
        pN.extend([Pn1, Pn2, Pn3])
        """if n <= (s - 1):
            pN = round((((pow((lamda / mu), n)) / (factorial(n))) * pCero), 4)
        elif n == s or n < (s + 1) or n == K:
            pN = round((((pow((lamda / mu), n)) / (factorial(s) * pow(s, n - s))) * pCero), 4)
        else:
            pN = 0"""
        Lq = round((((pCero * (pow((lamda / mu), s)) * p) / (self.factorial(s) * (pow((1 - p), 2))))
                   * (1 - pow(p, K - s) - (K - s) * pow(p, K - s) * (1 - p))), 4)

        if K <= (s - 1):
            pK = round(
                (((pow((lamda / mu), K)) / (self.factorial(K))) * pCero), 4)
        elif K == s or K < (s + 1) or K == K:
            pK = round(
                (((pow((lamda / mu), K)) / (self.factorial(s) * pow(s, (K - s)))) * pCero), 4)
        else:
            pK = 0
        lamdaE = round((lamda * (1 - pK)), 4)
        Wq = round((Lq / lamdaE), 4)
        W = round((Wq + (1 / mu)), 4)
        L = round((lamdaE * W), 4)
        print("p: " + str(p))
        #print("Cn: " + str(Cn) + ". Donde n = "+ str(n) + ", s = " + str(s) + " y K = " + str(K))
        print("Cn1: " + str(Cn1) + " para casos donde n = 0,1,2,...,s-1")
        print("Cn2: " + str(Cn2) + " para casos donde  n = s,s+1,...K")
        print("Cn3: " + str(Cn3) + " para casos donde  n > K")
        print("P0: " + str(pCero))
        #print("Pn: "+ str(pN) + ". Donde n = "+ str(n) + " y s = " + str(s))
        print("Pn1: " + str(Pn1) + " para casos donde n = 1,2,...,s-1")
        print("Pn2: " + str(Pn2) + " para casos donde n = s,s+1,...K")
        print("Pn3: " + str(Pn3) + " para casos donde  n > K")
        print("Número promedio de clientes en la cola (Lq): " +
              str(Lq) + " clientes")
        print("Número promedio de clientes en el sistema (L): " +
              str(L) + " clientes")
        print("Tiempo esperado en la cola (Wq): " + str(Wq) + " " + tiempo)
        print("Tiempo promeido en el sistema (W): " + str(W) + " " + tiempo)
        print("La tasa efectiva de arribo al sistema es (lammdaE): " +
              str(lamdaE) + " clientes por " + tiempo[:-1])

        arreglo_valores_UI = [p, Cn, pCero, pN, Lq, L, Wq, W, lamdaE]

        arreglo_tabla = [self.arreglo_titulo, arreglo_valores_UI]

        results = tk.Toplevel()
        results.title("Resultados")
        rows = []
        result_title = tk.Label(results, text='Resultados del Modelo M/M/S/K :', font=(
            "Castellar", 10)).grid(column=0, row=0, padx=7, pady=15, sticky="ew", columnspan=4)

        self.mmsK_iniciacionDeTabla(arreglo_tabla, results, tiempo, "m/m/1", 9)
        self.mmsK_tabla_latex(arreglo_tabla, results, 9)

    def m_m_1_frame(self, *args):
        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text'] = "m_m_1_frame"
        self.setHistoricoBtns("modelo_M_M_1.csv")

        for widget in self.frame.winfo_children():
            widget.destroy()

        # Display de los inputs necesarios para el método
        lambda_label = ttk.Label(self.frame,  text='Tasa de llegadas (lambda) :', font=(
            "Castellar", 8)).grid(column=0, row=1, padx=10, pady=20, sticky="e")
        lambda_input = tk.Entry(self.frame, width=20)
        lambda_input.grid(column=1, row=1, padx=40)

        mu_label = ttk.Label(self.frame,  text='Tasa de Servicio (mu) :', font=(
            "Castellar", 8)).grid(column=0, row=2, padx=10, pady=20, sticky="e")
        mu_input = tk.Entry(self.frame, width=20)
        mu_input.grid(column=1, row=2, padx=10)

        tiempo_label = ttk.Label(self.frame,  text='Unidad de Tiempo :', font=(
            "Castellar", 8)).grid(column=0, row=3, padx=10, pady=20, sticky="e")
        tiempo_input = tk.Entry(self.frame, width=20)
        tiempo_input.grid(column=1, row=3, padx=10)

        sumbit_btn = tk.Button(self.frame, text="Generar", font=(
            "Castellar", 8), command=lambda: self.aux_m_m_1_frame(lambda_input, mu_input, tiempo_input))
        sumbit_btn.grid(column=0, row=5, columnspan=3, pady=20)

    def aux_m_m_1_frame(self, lambda_input, mu_input, tiempo_input):
        # Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage = tk.Label(
            self.frame,  textvariable=self.errorText, font=("Castellar", 8), fg="red")
        if lambda_input.get() != '' and mu_input.get() != '' and tiempo_input.get() != '':
            try:
                x1 = float(lambda_input.get())
                x2 = float(mu_input.get())

            except:
                self.errorText.set('Lambda, mu y n deben ser números')
                self.errorMessage.grid(column=0, row=0, columnspan=2)
                return
            if self.comprobacion_Modelo_M_M_1(x1, x2):
                self.modelo_M_M_1(x1, x2, tiempo_input.get())
            # self.centrosCuadrados(x1,x2)
        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0, row=0, columnspan=2)

    def m_m_s_frame(self, *args):
        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text'] = "m_m_s_frame"
        self.setHistoricoBtns("modelo_M_M_s.csv")

        for widget in self.frame.winfo_children():
            widget.destroy()

        # Display de los inputs necesarios para el método
        lambda_label = ttk.Label(self.frame,  text='Tasa de llegadas (lambda) :', font=(
            "Castellar", 8)).grid(column=0, row=1, padx=10, pady=20, sticky="e")
        lambda_input = tk.Entry(self.frame, width=20)
        lambda_input.grid(column=1, row=1, padx=40)

        mu_label = ttk.Label(self.frame,  text='Tasa de Servicio (mu) :', font=(
            "Castellar", 8)).grid(column=0, row=2, padx=10, pady=20, sticky="e")
        mu_input = tk.Entry(self.frame, width=20)
        mu_input.grid(column=1, row=2, padx=10)

        tiempo_label = ttk.Label(self.frame,  text='Unidad de Tiempo :', font=(
            "Castellar", 8)).grid(column=0, row=3, padx=10, pady=20, sticky="e")
        tiempo_input = tk.Entry(self.frame, width=20)
        tiempo_input.grid(column=1, row=3, padx=10)

        server_label = ttk.Label(self.frame,  text='No. de Servidores :', font=(
            "Castellar", 8)).grid(column=0, row=4, padx=10, pady=20, sticky="e")
        server_input = tk.Entry(self.frame, width=20)
        server_input.grid(column=1, row=4, padx=10)

        sumbit_btn = tk.Button(self.frame, text="Generar", font=("Castellar", 8),
                               command=lambda: self.aux_m_m_s_frame(lambda_input, mu_input, tiempo_input, server_input))

        sumbit_btn.grid(column=0, row=6, columnspan=3, pady=20)

    def aux_m_m_s_frame(self, lambda_input, mu_input, tiempo_input, server_input):
        # Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage = tk.Label(
            self.frame,  textvariable=self.errorText, font=("Castellar", 8), fg="red")
        if lambda_input.get() != '' and mu_input.get() != '' and tiempo_input.get() != '' and server_input.get() != '':
            try:
                x1 = float(lambda_input.get())
                x2 = float(mu_input.get())
                x3 = int(server_input.get())

            except:
                self.errorText.set(
                    'Lambda, mu, n y el no. de servidores deben ser números')
                self.errorMessage.grid(column=0, row=0, columnspan=2)
                return
            if self.comprobacion_Modelo_M_M_s(x1, x2, x3):
                self.modelo_M_M_s(x1, x2, tiempo_input.get(), x3)

        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0, row=0, columnspan=2)

    def m_m_s_K_frame(self, *args):
        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text'] = "m_m_s_K_frame"
        self.setHistoricoBtns("modelo_M_M_s_K.csv")

        for widget in self.frame.winfo_children():
            widget.destroy()

        # Display de los inputs necesarios para el método
        lambda_label = ttk.Label(self.frame,  text='Tasa de llegadas (lambda) :', font=(
            "Castellar", 8)).grid(column=0, row=1, padx=10, pady=20, sticky="e")
        lambda_input = tk.Entry(self.frame, width=20)
        lambda_input.grid(column=1, row=1, padx=40)

        mu_label = ttk.Label(self.frame,  text='Tasa de Servicio (mu) :', font=(
            "Castellar", 8)).grid(column=0, row=2, padx=10, pady=20, sticky="e")
        mu_input = tk.Entry(self.frame, width=20)
        mu_input.grid(column=1, row=2, padx=10)

        tiempo_label = ttk.Label(self.frame,  text='Unidad de Tiempo :', font=(
            "Castellar", 8)).grid(column=0, row=3, padx=10, pady=20, sticky="e")
        tiempo_input = tk.Entry(self.frame, width=20)
        tiempo_input.grid(column=1, row=3, padx=10)

        server_label = ttk.Label(self.frame,  text='No. de Servidores :', font=(
            "Castellar", 8)).grid(column=0, row=4, padx=10, pady=20, sticky="e")
        server_input = tk.Entry(self.frame, width=20)
        server_input.grid(column=1, row=4, padx=10)

        k_label = ttk.Label(self.frame,  text='K :', font=("Castellar", 8)).grid(
            column=0, row=5, padx=10, pady=20, sticky="e")
        k_input = tk.Entry(self.frame, width=20)
        k_input.grid(column=1, row=5, padx=10)

        sumbit_btn = tk.Button(self.frame, text="Generar", font=("Castellar", 8),
                               command=lambda: self.aux_m_m_s_K_frame(lambda_input, mu_input, tiempo_input, k_input, server_input))

        sumbit_btn.grid(column=0, row=6, columnspan=3, pady=20)

    def aux_m_m_s_K_frame(self, lambda_input, mu_input, tiempo_input, k_input, server_input):
        # Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage = tk.Label(
            self.frame,  textvariable=self.errorText, font=("Castellar", 8), fg="red")
        if lambda_input.get() != '' and mu_input.get() != '' and tiempo_input.get() != '' and k_input.get() != '' and server_input.get() != '':
            try:
                x1 = float(lambda_input.get())
                x2 = float(mu_input.get())
                x3 = int(server_input.get())
                x4 = int(k_input.get())
            except:
                self.errorText.set(
                    'Lambda, mu, n y el no. de servidores deben ser números')
                self.errorMessage.grid(column=0, row=0, columnspan=2)
                return
            if self.comprobacion_Modelo_M_M_s_K(x1, x2, x3, x4):
                self.modelo_M_M_s_K(x1, x2, tiempo_input.get(), x3, x4)
        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0, row=0, columnspan=2)

    def m_G_1_frame(self, *args):

        # Loop para limpiar los widgets del frame para cambiar entre las opciones del menu
        self.frame['text'] = "m_G_1_frame"
        self.setHistoricoBtns("modelo_M_G_1.csv")

        for widget in self.frame.winfo_children():
            widget.destroy()

        # Display de los inputs necesarios para el método
        lambda_label = ttk.Label(self.frame,  text='Tasa de llegadas (lambda) :', font=(
            "Castellar", 8)).grid(column=0, row=1, padx=10, pady=20, sticky="e")
        lambda_input = tk.Entry(self.frame, width=20)
        lambda_input.grid(column=1, row=1, padx=40)

        mu_label = ttk.Label(self.frame,  text='Tasa de Servicio (mu) :', font=(
            "Castellar", 8)).grid(column=0, row=2, padx=10, pady=20, sticky="e")
        mu_input = tk.Entry(self.frame, width=20)
        mu_input.grid(column=1, row=2, padx=10)

        tiempo_label = ttk.Label(self.frame,  text='Unidad de Tiempo :', font=(
            "Castellar", 8)).grid(column=0, row=3, padx=10, pady=20, sticky="e")
        tiempo_input = tk.Entry(self.frame, width=20)
        tiempo_input.grid(column=1, row=3, padx=10)

        server_label = ttk.Label(self.frame,  text='No. de Servidores :', font=(
            "Castellar", 8)).grid(column=0, row=4, padx=10, pady=20, sticky="e")
        server_input = tk.Entry(self.frame, width=20)
        server_input.grid(column=1, row=4, padx=10)

        n_label = ttk.Label(self.frame,  text='N :', font=("Castellar", 8)).grid(
            column=0, row=5, padx=10, pady=20, sticky="e")
        n_input = tk.Entry(self.frame, width=20)
        n_input.grid(column=1, row=5, padx=10)

        sumbit_btn = tk.Button(self.frame, text="Generar", font=("Castellar", 8),
                               command=lambda: self.aux_m_G_1_frame(lambda_input, mu_input, tiempo_input, n_input, server_input))
        sumbit_btn.grid(column=0, row=6, columnspan=3, pady=20)

    def aux_m_G_1_frame(self, lambda_input, mu_input, tiempo_input, n_input, server_input):
        # Método auxiliar para extraer los datos de los inputs y validar los datos dentro decada input
        self.errorText.set(' ')
        self.errorMessage = tk.Label(
            self.frame,  textvariable=self.errorText, font=("Castellar", 8), fg="red")
        if lambda_input.get() != '' and mu_input.get() != '' and tiempo_input.get() != '' and n_input.get() != '' and server_input.get() != '':
            try:
                x1 = float(lambda_input.get())
                x2 = float(mu_input.get())
                x3 = float(server_input.get())
                x4 = float(n_input.get())
            except:
                self.errorText.set(
                    'Lambda, mu, n y el no. de servidores deben ser números')
                self.errorMessage.grid(column=0, row=0, columnspan=2)
                return
            if True:
                print("M/G/1 DEBUG")
                #self.modelo_M_M_1(x1, x2, tiempo_input.get(), x4)

        else:
            # Mensaje de error para inputs vacios
            self.errorText.set('Favor de llenar todos los rubros')
            self.errorMessage.grid_configure(column=0, row=0, columnspan=2)

    def option_changed(self, *args):
        if self.option.get() == self.menu[0]:
            self.m_m_1_frame()
        elif self.option.get() == self.menu[1]:
            self.m_m_s_frame()
        elif self.option.get() == self.menu[2]:
            self.m_m_s_K_frame()
        elif self.option.get() == self.menu[3]:
            self.m_G_1_frame()

    def setHistoricoBtns(self, path_to_csv):
        self.clearBtn['command'] = lambda: self.clearData(path_to_csv)
        self.showBtn['command'] = lambda: self.showGraph(path_to_csv)
        self.clearBtn.grid(column=2, row=1, sticky='n', pady=(30, 0))
        self.showBtn.grid(column=2, row=2, sticky='n')


if __name__ == "__main__":
    app = App()
    app.mainloop()

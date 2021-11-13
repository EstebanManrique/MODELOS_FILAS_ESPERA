import os
import csv
import matplotlib.pyplot as plt
from numpy import double

nombresArchivos = ["modelo_M_M_1.csv", "modelo_M_M_s.csv", "modelo_M_M_s_K.csv", "modelo_M_G_1.csv"]

def comprobacionPn(clientes, caso):
    if clientes < 0:
        print("El numero de clientes no puede ser negativo")
        return False
    if type(clientes) != int:
        print("El numero de clientes debe ser un numero entero positivo")
        return False
    if clientes == 0 and caso == "<":
        print("No puede haber menos clientes que Cero")
        return False
    return True

# --- MM1 ---
def modelo_M_M_1(lamda, mu, tiempo): #Se elimina n
    if comprobacion_Modelo_M_M_1(lamda, mu):
        s = 1
        p = round((lamda / mu), 4)
        Cn = str(p) + " ** n" #round((pow(p, n)),4) 
        pCero = round((1 - p), 4)
        pN = str(pCero) + "(" + str(p) + " ** n)"    #round((pCero * pow(p, n)), 4)
        Lq = round((pow(lamda, 2) / (mu * (mu - lamda))), 4)
        L = round((lamda / (mu - lamda)), 4)
        Wq = round((lamda /(mu * (mu - lamda))), 4)
        W = round((1 / (mu - lamda)), 4)

        print("p: "+ str(p))
        print("Cn: " + str(Cn))
        print("P0: "+ str(pCero))
        print("Pn: "+ str(pN))
        print("Número promedio de clientes en la cola (Lq): "+ str(Lq) + " clientes") 
        print("Número promedio de clientes en el sistema (L): "+ str(L) + " clientes")
        print("Tiempo esperado en la cola (Wq): "+ str(Wq) + " " + tiempo)
        print("Tiempo promeido en el sistema (W): "+ str(W) + " " + tiempo)

        arreglo_valores_UI = [p, Cn, pCero, pN, Lq, L, Wq, W]
        return arreglo_valores_UI

def calculo_Pn_Modelo_M_M_1(pCero, p, clientes, caso): #caso aqui puede ser "=", ">" o "<"
    if comprobacionPn(clientes, caso):
        if caso == "=":
            if clientes == 0:
                pN = pCero
            else:
                pN = round((pCero * pow(p, clientes)), 4)
        elif caso == ">":
            if clientes == 0:
                pN = 1 - pCero
            else:
                pN = 1
                acumulado = pCero
                for cliente in range(1, clientes + 1):
                    acumulado += round((pCero * pow(p, cliente)), 4)
                pN = pN - acumulado
        else:
            if clientes == 1:
                pN = pCero
            else:
                pN = pCero
                for cliente in range(1, clientes+1):
                    pN += round((pCero * pow(p, cliente)), 4)
        print(round(pN, 4))
        return round(pN, 4)

def comprobacion_Modelo_M_M_1(lamda, mu):
    if (((type(lamda) != (int)) and (type(lamda) != (float))) or ((type(mu) != (int)) and (type(mu) != (float)))):
        print("Lambda y Mu deben ser numeros Enteros/Decimales Positivos")
        return False
    if(lamda < 0 or mu < 0):
        print("El sistema NO puede aceptar valores Negativos")
        return False  
    if(lamda > mu or lamda == mu):
        print("El sistema siendo planeteado NO es estable. Lamda debe ser menor a mu")
        return False
    return True

# --- MMS ---
def modelo_M_M_s(lamda, mu, tiempo, s):
    if comprobacion_Modelo_M_M_s(lamda, mu, s):
        p = round((lamda / (s * mu)), 4)
        Cn = []
        Cn1 = "(" + str(round((lamda/mu), 4)) + " ** n) / n!"
        Cn2 = "(" + str(round((lamda/mu), 4)) + " ** n) / (" + str(factorial(s)) + " * (" + str(s) + " ** (n - " + str(s) + ")))"
        Cn.extend([Cn1, Cn2]) ##Cn1 es para casos donde n = 1,2,...,s-1 y Cn2 es para casos donde n = s,s+1,...
        """if n <= (s - 1):
            Cn = round((pow(lamda/mu, n) / factorial(n)),4)
        else:
            Cn = round((pow(lamda/mu, n) / (factorial(s) * pow(s, (n-s)))), 4)"""
        primerTerminoPCero = 0
        for index in range (0, s): #el ciclo solo hace hasta s - 1
            primerTerminoPCero += (pow(lamda/mu, index) / factorial(index))
        pCero = round((1 / (primerTerminoPCero + (pow(lamda/mu, s) / factorial(s)) * (1 / (1 - (lamda / (s * mu)))))), 4)
        pN = []
        Pn1 = "((" + str(round((lamda/mu), 4)) + " ** n) / n!) * " + str(pCero)
        Pn2 = "((" + str(round((lamda/mu), 4)) + " ** n) / (" + str(factorial(s)) + " * (" + str(s) + " ** (n - " + str(s) + ")))) * " + str(pCero)
        pN.extend([Pn1, Pn2]) ##Pn1 es para casos donde 0 <= n < s y Pn2 es para casos donde n >= s
        Lq = round(((pCero * pow(lamda / mu, s) * p) / (factorial(s) * pow((1 - p), 2))), 4)
        L = round((Lq + (lamda / mu)), 4)
        Wq = round((Lq / lamda), 4)
        W = round((Wq + (1/mu)), 4)

        print("p: "+ str(p))
        #print("Cn: " + str(Cn) + ". Donde n = "+ str(n) + " y s = " + str(s))
        print("Cn1: " + str(Cn1) + " para casos donde n = 1,2,...,s-1")
        print("Cn2: " + str(Cn2) + " para casos donde n = s,s+1,...")
        print("P0: " + str(pCero))
        #print("Pn: "+ str(pN) + ". Donde n = "+ str(n) + " y s = " + str(s))
        print("Pn1: " + str(Pn1) + " para casos donde 0 <= n < s")
        print("Pn2: " + str(Pn2) + " para casos donde n >= s")
        print("Número promedio de clientes en la cola (Lq): "+ str(Lq) + " clientes")
        print("Número promedio de clientes en el sistema (L): "+ str(L) + " clientes")
        print("Tiempo esperado en la cola (Wq): "+ str(Wq) + " " + tiempo)
        print("Tiempo promeido en el sistema (W): "+ str(W) + " " + tiempo)

        arreglo_valores_UI = [p, Cn, pCero, pN, Lq, L, Wq, W]
        return arreglo_valores_UI

def calculo_Pn_Modelo_M_M_s(pCero, lamda, mu, s, clientes, caso):
    if comprobacionPn(clientes, caso):
        if caso == "=":
            if clientes == 0:
                pN = pCero
            elif (clientes <= 0) and (s > clientes):
                pN = round((((pow(lamda/mu,clientes)) / factorial(clientes)) * pCero), 4)
            else:
                pN = round((((pow(lamda/mu,clientes)) / (factorial(s) * pow(s, clientes-s))) * pCero), 4)
        elif caso == ">":
            if clientes == 0:
                pN = 1 - pCero
            else:
                pN = 1
                acumulado = pCero
                for cliente in range(1, clientes + 1):
                    if (cliente <= 0) and (s > cliente):
                        acumulado += round((((pow(lamda/mu,cliente)) / factorial(cliente)) * pCero), 4)
                    else:
                        acumulado += round((((pow(lamda/mu,cliente)) / (factorial(s) * pow(s, cliente-s))) * pCero), 4)
                pN = pN - acumulado
        else:
            if clientes == 1:
                pN = pCero
            else:
                pN = pCero
                for cliente in range(1, clientes+1):
                    if (cliente <= 0) and (s > cliente):
                        pN += round((((pow(lamda/mu,cliente)) / factorial(cliente)) * pCero), 4)
                    else:
                        pN+= round((((pow(lamda/mu,cliente)) / (factorial(s) * pow(s, cliente-s))) * pCero), 4)
        print(round(pN, 4))
        return(round(pN, 4))

def comprobacion_Modelo_M_M_s(lamda, mu, s):
    if (((type(lamda) != (int)) and (type(lamda) != (float))) and ((type(mu) != (int)) and (type(mu) != (float)))):
        print("Lambda y Mu deben ser numeros Enteros/Decimales Positivos")
        return False
    if(lamda < 0 or mu < 0):
        print("El sistema NO puede aceptar valores Negativos")
        return False  
    if(mu * s <= lamda):
        print("El sistema siendo planeteado NO es estable. Lamda debe ser menor a el PRODUCTO de Mu y s")
        return False
    if(type(s) != int):
        print("El valor de s debe ser ENTERO")
        return False
    if(s < 1):
        print("El valor de s es menor a 1. NO es aceptable")
        return False
    return True

def factorial(numero):
    factorial = 1
    for i in range(1, numero + 1):
        factorial = factorial * i
    return factorial

# --- MMsK ---
def modelo_M_M_s_K(lamda, mu, tiempo, s, K):
    if comprobacion_Modelo_M_M_s_K(lamda, mu, s, K):
        p = round((lamda / (s * mu)), 4)
        Cn = []
        Cn1 = "(" + str(round((lamda/mu), 4)) + " ** n) / n!"
        Cn2 = "(" + str(round((lamda/mu), 4)) + " ** n) / (" + str(factorial(s)) + " * (" + str(s) + " ** (n - " + str(s) + ")))"
        Cn3 = 0
        Cn.extend([Cn1, Cn2, Cn3]) ##Cn1 es para casos donde n = 0,1,2,...,s-1,  Cn2 es para casos donde n = s,s+1,...K y Cn3 es para casos donde n > K
        """if n <= (s - 1):
            Cn = round(((pow((lamda / mu), n)) / (factorial(n))), 4)
        elif n == s or n < (s + 1) or n == K:
            Cn = round(((pow((lamda / mu), n)) / (factorial(s) * pow(s, n-s))), 4)
        else:
            Cn = 0"""
        primerTerminoPCero = 0
        for index in range (0, (s+1)): #el ciclo solo llega a s
            primerTerminoPCero += (pow((lamda / mu), index)) / (factorial(index))
        tercerTerminoPCero = 0
        for index in range((s+1), (K + 1)): #el ciclo solo llega a K
            tercerTerminoPCero += pow(lamda / (s * mu), (index - s))
        pCero = round((1 / (primerTerminoPCero + (pow((lamda / mu), s) / factorial(s)) * tercerTerminoPCero)), 4)
        pN = []
        Pn1 = "((" + str(round((lamda/mu), 4)) + " ** n) / n!) * " + str(pCero)
        Pn2 = "((" + str(round((lamda/mu), 4)) + " ** n) / (" + str(factorial(s)) + " * (" + str(s) + " ** (n - " + str(s) + ")))) * " + str(pCero)
        Pn3 = 0
        pN.extend([Pn1, Pn2, Pn3]) ##Pn1 es para casos donde n = 1,2,...,s-1, Pn2 es para casos donde n = s,s+1,...K y Pn3 es para casos donde n > K
        """if n <= (s - 1):
            pN = round((((pow((lamda / mu), n)) / (factorial(n))) * pCero), 4)
        elif n == s or n < (s + 1) or n == K:
            pN = round((((pow((lamda / mu), n)) / (factorial(s) * pow(s, n - s))) * pCero), 4)
        else:
            pN = 0"""
        Lq = round((((pCero * (pow((lamda / mu), s)) * p) / (factorial(s) * (pow((1 - p), 2)))) * (1 - pow(p, K - s) - (K- s) * pow(p, K - s) * (1 - p))), 4)
        
        if K <= (s - 1):
            pK = round((((pow((lamda / mu), K)) / (factorial(K))) * pCero), 4)
        elif K == s or K < (s + 1) or K == K:
            pK = round((((pow((lamda / mu), K)) / (factorial(s) * pow(s, (K - s)))) * pCero), 4)
        else:
            pK = 0
        lamdaE = round((lamda * (1 - pK)),4 )
        Wq = round((Lq / lamdaE), 4)
        W = round((Wq + (1 / mu)), 4)
        L = round((lamdaE * W), 4)

        print("p: "+ str(p))
        #print("Cn: " + str(Cn) + ". Donde n = "+ str(n) + ", s = " + str(s) + " y K = " + str(K))
        print("Cn1: " + str(Cn1) + " para casos donde n = 0,1,2,...,s-1")
        print("Cn2: " + str(Cn2) + " para casos donde  n = s,s+1,...K")
        print("Cn3: " + str(Cn3) + " para casos donde  n > K")
        print("P0: " + str(pCero))
        #print("Pn: "+ str(pN) + ". Donde n = "+ str(n) + " y s = " + str(s))
        print("Pn1: " + str(Pn1) + " para casos donde n = 1,2,...,s-1")
        print("Pn2: " + str(Pn2) + " para casos donde n = s,s+1,...K")
        print("Pn3: " + str(Pn3) + " para casos donde  n > K")
        print("Número promedio de clientes en la cola (Lq): "+ str(Lq) + " clientes")
        print("Número promedio de clientes en el sistema (L): "+ str(L) + " clientes")
        print("Tiempo esperado en la cola (Wq): "+ str(Wq) + " " + tiempo)
        print("Tiempo promeido en el sistema (W): "+ str(W) + " " + tiempo)
        print("La tasa efectiva de arribo al sistema es (lammdaE): "+ str(lamdaE) + " clientes por " + tiempo[:-1])

        arreglo_valores_UI = [p, Cn, pCero, pN, Lq, L, Wq, W]
        return arreglo_valores_UI

def calculo_Pn_Modelo_M_M_s_K(pCero, lamda, mu, s, K, clientes, caso):
    if comprobacionPn(clientes, caso):
        if caso == "=":
            if clientes == 0:
                pN = pCero
            elif clientes <= (s - 1):
                pN = round((((pow((lamda / mu), clientes)) / (factorial(clientes))) * pCero), 4)
            elif clientes == s or clientes < (s + 1) or clientes == K:
                pN = round((((pow((lamda / mu), clientes)) / (factorial(s) * pow(s, clientes - s))) * pCero), 4)
            else:
                pN = 0
        elif caso == ">":
            if clientes == 0:
                pN = 1 - pCero
            else:
                pN = 1
                acumulado = pCero
                for cliente in range(1, clientes + 1):
                    if cliente <= (s - 1):
                        acumulado += round((((pow((lamda / mu), cliente)) / (factorial(cliente))) * pCero), 4)
                    elif cliente == s or cliente < (s + 1) or cliente == K:
                        acumulado += round((((pow((lamda / mu), cliente)) / (factorial(s) * pow(s, cliente - s))) * pCero), 4)
                    else:
                        acumulado += 0
                pN = pN - acumulado
        else:
            if clientes == 1:
                pN = pCero
            else:
                pN = pCero
                for cliente in range(1, clientes + 1):
                    if cliente <= (s - 1):
                        pN += round((((pow((lamda / mu), cliente)) / (factorial(cliente))) * pCero), 4)
                    elif cliente == s or cliente < (s + 1) or cliente == K:
                        pN += round((((pow((lamda / mu), cliente)) / (factorial(s) * pow(s, cliente - s))) * pCero), 4)
                    else:
                        pN += 0
        print(round(pN, 4))
        return(round(pN, 4))

def comprobacion_Modelo_M_M_s_K(lamda, mu, s, K):
    if (((type(lamda) != (int)) or (type(lamda) != (float))) and ((type(mu) != (int)) or (type(mu) != (float)))):
        print("Lambda y Mu deben ser numeros Enteros/Decimales Positivos")
        return False
    if(lamda < 0 or mu < 0):
        print("El sistema NO puede aceptar valores Negativos")
        return False  
    if(mu * s <= lamda):
        print("El sistema siendo planeteado NO es estable. Lamda debe ser menor a mu")
        return False
    if(type(K) != int):
        print("El valor de K debe ser ENTERO")
        return False
    if(K < 0):
        print("El valor de K es menor a 0. NO es aceptable")
        return False
    if(type(s) != int):
        print("El valor de s debe ser ENTERO")
        return False
    if(s < 0):
        print("El valor de s es menor a 0. NO es aceptable")
        return False
    if(s > K):
        print("El valor de K debe ser menor o igual a S para este modelo")
        return False
    return True

# --- MG1 ---
def modelo_M_G_1(lamda, mu, tiempo, desviacion):
    if comprobacion_Modelo_M_G_1(lamda, mu, desviacion):
        s = 1 #Pero hay que checar svenx
        p = round((lamda / mu), 4)
        pCero = round((1 - p), 4)
        pN = str(pCero) + "(" + str(p) + " ** n)"    #round((pCero * pow(p, n)), 4)
        Lq = round((((pow(lamda,2) * pow(desviacion,2))+ pow(p,2))/(2*(1-p))) , 4) #formula de pollaczek khintchine
        L = round((p + Lq), 4)
        Wq = round((Lq/lamda), 4)
        W = round((Wq + (1/mu)), 4)

        print("------- Modelo M/G/1----------")
        print("p: "+ str(p))
        print("P0: "+ str(pCero))
        print("Pn: "+ str(pN))
        print("Número promedio de clientes en la cola (Lq): "+ str(Lq) + " clientes") 
        print("Número promedio de clientes en el sistema (L): "+ str(L) + " clientes")
        print("Tiempo esperado en la cola (Wq): "+ str(Wq) + " " + tiempo)
        print("Tiempo promeido en el sistema (W): "+ str(W) + " " + tiempo)

        arreglo_valores_UI = [p, pCero, pN, Lq, L, Wq, W]
        return arreglo_valores_UI

def calculo_Pn_Modelo_M_G_1(pCero, p, clientes, caso):
    if comprobacionPn(clientes, caso):
        return calculo_Pn_Modelo_M_M_1(pCero, p, clientes, caso)

def comprobacion_Modelo_M_G_1(lamda, mu, desviacion):
    if (((type(lamda) != (int)) and (type(lamda) != (float))) or ((type(mu) != (int)) and (type(mu) != (float)))):
        print("Lambda y Mu deben ser numeros Enteros/Decimales Positivos")
        return False
    if(lamda < 0 or mu < 0):
        print("El sistema NO puede aceptar valores Negativos")
        return False  
    if(lamda > mu or lamda == mu):
        print("El sistema siendo planeteado NO es estable. Lamda debe ser menor a mu")
        return False
    if((type(desviacion) != int) and (type(desviacion) != float)):
        print("El valor de la desviacion debe ser ENTERO/Decimal")
        return False
    if(desviacion < 0):
        print("El sistema M/G/1 tiene que tener una desv. estandar mayor a 0 ")
        return False
    return True

# --- MD1 ---
def modelo_M_D_1(lamda, mu, tiempo):
    if comprobacion_Modelo_M_D_1(lamda, mu):
        s = 1 #Pero hay que checar svenx

        p = round((lamda / mu), 4)
        pCero = round((1 - p), 4)
        pN = str(pCero) + "(" + str(p) + " ** n)"    #round((pCero * pow(p, n)), 4)
        Lq = round((pow(p,2)/(2*(1-p))) , 4) #formula de pollaczek khintchine con desv = 0
        L = round((p + Lq), 4)
        Wq = round((Lq/lamda), 4)
        W = round((Wq + (1/mu)), 4)

        print("------- Modelo M/D/1----------")
        print("p: "+ str(p))
        print("P0: "+ str(pCero))
        print("Pn: "+ str(pN))
        print("Número promedio de clientes en la cola (Lq): "+ str(Lq) + " clientes") 
        print("Número promedio de clientes en el sistema (L): "+ str(L) + " clientes")
        print("Tiempo esperado en la cola (Wq): "+ str(Wq) + " " + tiempo)
        print("Tiempo promeido en el sistema (W): "+ str(W) + " " + tiempo)

        arreglo_valores_UI = [p, pCero, pN, Lq, L, Wq, W]
        return arreglo_valores_UI

def calculo_Pn_Modelo_M_D_1(pCero, p, clientes, caso):
    if comprobacionPn(clientes, caso):
        return calculo_Pn_Modelo_M_M_1(pCero, p, clientes, caso)

def comprobacion_Modelo_M_D_1(lamda, mu):
    if (((type(lamda) != (int)) and (type(lamda) != (float))) or ((type(mu) != (int)) and (type(mu) != (float)))):
        print("Lambda y Mu deben ser numeros Enteros/Decimales Positivos")
        return False
    if(lamda < 0 or mu < 0):
        print("El sistema NO puede aceptar valores Negativos")
        return False  
    if(lamda > mu or lamda == mu):
        print("El sistema siendo planeteado NO es estable. Lamda debe ser menor a mu")
        return False
    return True

# --- MEks ---
def modelo_M_Ek_s(lamda, mu, s, tiempo, k):
    if comprobacion_modelo_M_Ek_s(lamda,mu,k,s):
        p = round((lamda / (s * mu)), 4)
        pCero = round((1 - p), 4)
        pN = str(pCero) + "(" + str(p) + " ** n)"    #round((pCero * pow(p, n)), 4)
        Lq = round((((1 + k) / (2 * k)) * ((pow(lamda,2)) / (mu * (mu - lamda)))), 4) #formula de pollaczek khintchine para modelo Erlang
        Wq = round((Lq/ lamda), 4)
        W = round((Wq + (1/mu)), 4)
        L = round((lamda * W), 4)

        print("------- Modelo M/Ek/s----------")
        print("p: "+ str(p))
        print("P0: "+ str(pCero))
        print("Pn: "+ str(pN))
        print("Número promedio de clientes en la cola (Lq): "+ str(Lq) + " clientes") 
        print("Número promedio de clientes en el sistema (L): "+ str(L) + " clientes")
        print("Tiempo esperado en la cola (Wq): "+ str(Wq) + " " + tiempo)
        print("Tiempo promeido en el sistema (W): "+ str(W) + " " + tiempo)

        arreglo_valores_UI = [p, pCero, pN, Lq, L, Wq, W]
        return arreglo_valores_UI

def calculo_Pn_Modelo_M_Ek_s(pCero, p, clientes, caso):
    if comprobacionPn(clientes, caso):
        return calculo_Pn_Modelo_M_M_1(pCero, p, clientes, caso)

def comprobacion_modelo_M_Ek_s(lamda, mu, K,s):
    if ((type(lamda) != (int)) and (type(lamda) != (float))) and ((type(mu) != (int)) and (type(mu) != (float))):
        print("Lambda y Mu deben ser numeros Enteros/Decimales Positivos")
        return False
    if(lamda < 0 or mu < 0):
        print("El sistema NO puede aceptar valores Negativos")
        return False  
    if(mu * s <= lamda):
        print("El sistema siendo planeteado NO es estable. Lamda debe ser menor a mu")
        return False
    if(type(K) != int):
        print("El valor de K debe ser ENTERO")
        return False
    if(K < 0):
        print("El valor de K es menor a 0. NO es aceptable")
        return False
    if(type(s) != int):
        print("El valor de s debe ser ENTERO")
        return False
    if(s < 0):
        print("El valor de s es menor a 0. NO es aceptable")
        return False
    return True

# --- Costos ---


def escrituraCsv(archivo, tiempoCola, tiempoSistema):
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
            contenido.extend([str(1), str(float(tiempoCola)), str((float(tiempoSistema)))])
            for index in contenido:
                escritor.writerow([index])

def resetearCsv(archivo):
    if os.path.exists(archivo):
        os.remove(archivo)
    else:
        print("El archivo estadistico ya esta reseteado")

def generarGraficaTiempos(archivo):
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

        promedioCola = promedio(infoArchivo[1])
        promedioSistema = promedio(infoArchivo[2])
        puntosCola = []
        puntosSistema = []
        for index in range(0, numeroPuntos):
            puntosCola.append(promedioCola)
            puntosSistema.append(promedioSistema)

        plt.plot(indiceHistoricos, infoArchivo[1], label = "Tiempo en Cola")
        plt.plot(indiceHistoricos, infoArchivo[2], label = "Tiempo en Sistema")
        plt.plot(indiceHistoricos, puntosCola, label = "Promedio en Cola (" + str(promedioCola)+")")
        plt.plot(indiceHistoricos, puntosSistema, label = "Promedio en Sistema (" + str(promedioSistema)+")")
        plt.xlabel("Numero de simulacion")
        plt.ylabel("Unidades de tiempo")
        plt.xticks(range(indiceHistoricos[0], indiceHistoricos[len(indiceHistoricos) - 1] + 1))
        plt.legend()
        plt.show()
    else:
        print("No se tienen registros historicos para este modelo eb particular")

def promedio(lista):
    suma = 0
    for element in lista:
        suma += element
    return (suma / len(lista))


#calculo_Pn_Modelo_M_M_1(0.090909, (5/6), 3, ">")
#comprobacion_Modelo_M_M_1(2.2,10)

#modelo_M_M_s(100,60,"h",2)
#calculo_Pn_Modelo_M_M_s(0.090909, 100, 60, 2, 3, "<")

#calculo_Pn_Modelo_M_M_s_K(0.14, 10, 7, 2, 4, 4, "=")

#modelo_M_G_1(3,5,"horas",0.1)
#modelo_M_Ek_s(3,5,1,"horas",4)
#modelo_M_D_1(3,5,"horas")

#modelo_M_M_1(2,3,"horas")
#modelo_M_M_s(3687,1850,"horas",2)
#modelo_M_M_s_K(2,3,"horas",1,3)

#Segundo parametro es Lq y Tercer parametro es L                                
#escrituraCsv(nombresArchivos[0], 10, 8) 
#escrituraCsv(nombresArchivos[1], 85, 52)
#escrituraCsv(nombresArchivos[2], 98, 102)
#escrituraCsv(nombresArchivos[3], 98, 102)

#resetearCsv(nombresArchivos[0])
#resetearCsv(nombresArchivos[1])
#resetearCsv(nombresArchivos[2])
#resetearCsv(nombresArchivos[3])

#generarGraficaTiempos(nombresArchivos[0])
#generarGraficaTiempos(nombresArchivos[1])
#generarGraficaTiempos(nombresArchivos[2])
#generarGraficaTiempos(nombresArchivos[3])
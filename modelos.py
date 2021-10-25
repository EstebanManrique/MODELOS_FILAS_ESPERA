#lambda: tasa media de llegadas(numeros de clientes esperados por unidad de tiempo)
#mu: tasa media de servicios(numero de clientes que completan el servicio por unidad de tiempo)
#tiempo: define la unidad de tiempo a ser utilizada por el modelo (segundos, minutos, días, semanas, meses)
#n: ??
def modelo_M_M_1(lamda, mu, tiempo,n):
    if comprobacion_Modelo_M_M_1(lamda, mu, n):
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
        return arreglo_valores_UI

def comprobacion_Modelo_M_M_1(lamda, mu, n):
    if(lamda < 0 or mu < 0):
        print("El sistema NO puede aceptar valores Negativos")
        return False  
    if(lamda > mu or lamda == mu):
        print("El sistema siendo planeteado NO es estable. Lambda debe ser menor a mu")
        return False
    if(n < 0):
        print("El valor de n es menor a 0. NO es aceptable")
        return False;
    if(n % 1 != 0):
        print("El valor de n NO puede ser decimal")
        return False; 
    return True

def modelo_M_M_s(lamda, mu, tiempo, s, n):
    if comprobacion_Modelo_M_M_s(lamda, mu, s, n):
        p = lamda / (s * mu)
        if n >= (s - 1):
            Cn = round((pow(lamda/mu, n) / factorial(n)),4)
        else:
            Cn = round((pow(lamda/mu, n) / (factorial(s) * pow(s, (n-s)))), 4)
        primerTerminoPCero = 0
        for index in range (0, s): #el ciclo solo hace hasta s - 1
            primerTerminoPCero += (pow(lamda/mu, index) / factorial(index))
        pCero = round((1 / (primerTerminoPCero + (pow(lamda/mu, s) / factorial(s)) * (1 / (1 - (lamda / (s * mu)))))), 4)
        if n >= 0 and n < s:
            pN = round((((pow(lamda/mu,n)) / factorial(n)) * pCero), 4)
        else:
            pN = round((((pow(lamda/mu,n)) / (factorial(s) * pow(s, n-s))) * pCero), 4)
        Lq = round(((pCero * pow(lamda / mu, s) * p) / (factorial(s) * pow((1 - p), 2))), 4)
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
        return arreglo_valores_UI

def comprobacion_Modelo_M_M_s(lamda, mu, s, n):
    if(lamda < 0 or mu < 0):
        print("El sistema NO puede aceptar valores Negativos")
        return False  
    """if(lamda > mu or lamda == mu):
        print("El sistema siendo planeteado NO es estable. Lambda debe ser menor a mu")
        return False"""
    if(mu * s < lamda):
        print("El sistema siendo planeteado NO es estable. Lambda debe ser menor a mu")
        return False
    if(n < 0):
        print("El valor de n es menor a 0. NO es aceptable")
        return False;
    if(n % 1 != 0):
        print("El valor de n NO puede ser decimal")
        return False; 
    if(s < 0):
        print("El valor de s es menor a 0. NO es aceptable")
        return False;
    if(s % 1 != 0):
         print("El valor de s NO puede ser decimal")
         return False; 
    return True

def factorial(numero):
    factorial = 1
    for i in range(1, numero + 1):
        factorial = factorial * i
    return factorial

#modelo_M_M_1(2,3,"horas",1)
modelo_M_M_s(3687,1850,"horas",2,1)
    
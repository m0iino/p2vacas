# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 00:17:09 2020

@author: moino
"""
import sys
import gramatica3 as g
import ts as TS
import editor as edit
from expresiones import *
from instrucciones import *
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from anytree.exporter import UniqueDotExporter
from graphviz import Digraph
cadena = ""
errores = []
cont_t=0
codigo3d = ""
def procesar_imprimir(instr, ts) :
    global cadena
    val = resolver_expresion_aritmetica(instr.cad, ts)
    print(' ', val,'\n')
    cadena = cadena+'> ' + str(val) +'\n'
    #print(cadena)

def getCadena():
    global cadena
    #print("get cadena:",cadena)
    return cadena
    
def procesar_borrar(instr,ts):
    #print("procesar borrar: ")
    ts.borrar(instr.cad.id)
    

def procesar_definicion(instr, ts) :
    print("tamaño:",len(instr.id))
    cont = 0
    for i in instr.id:
        print("id:",i.id)
        cont += 1
        print("procesar definicion: ",i.id,instr.tipo)
        simbolo = TS.Simbolo(i.id, instr.tipo, 0)      # inicializamos con 0 como valor por defecto
        ts.agregar(simbolo)
    print("definicion procesada")

def procesar_asignacion(instr,ts) :
    val = resolver_expresion_aritmetica(instr.expNumerica, ts)
    print("procesar asignacion :",instr.id,"=",val)
    if isinstance(instr.expNumerica, AccesoArreglo):
        #print("es arreglo")
        if ts.existe(instr) :
            print("existe solo se actualiza",ts.obtener(instr.id).tipo,"expresion es tipo:",instr.expNumerica.tipo)
            if ts.obtener(instr.id).tipo ==  instr.expNumerica.tipo:
                print("son int")
                simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
                ts.actualizar(simbolo)
            elif ts.obtener(instr.id).tipo == instr.expNumerica.tipo:
                print("son float")
                simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
                ts.actualizar(simbolo)    
            elif ts.obtener(instr.id).tipo ==instr.expNumerica.tipo :
                print("son char")
                simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
                ts.actualizar(simbolo)  
            elif ts.obtener(instr.id).tipo == "TIPO_DATO.CARACTER" and instr.expNumerica.tipo == TS.TIPO_DATO.CADENA:
                print("son char arreglo")
                simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
                ts.actualizar(simbolo)    
            else:
                print("no son del mismo tipo aca")
                err = "Error de tipos \'" + str(ts.obtener(instr.id).tipo)+ "\' con \'" +str(instr.expNumerica.tipo)+"\' en la linea: "+str(instr.expNumerica.linea)
                print(err)
                errores.append(err)

        else:
            print("no existe la variable, no se asignara")
            #simbolo = TS.Simbolo(instr.id,instr.expNumerica.expNumerica.tipo, val)
            #ts.agregar(simbolo) 
    else:

        if ts.existe(instr) :
            print("existe solo se actualiza",ts.obtener(instr.id).tipo,"expresion es tipo:",instr.expNumerica.tipo)
            if ts.obtener(instr.id).tipo ==  instr.expNumerica.tipo and instr.expNumerica.tipo == TS.TIPO_DATO.NUMERO:
                print("son int")
                simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
                ts.actualizar(simbolo)
            elif ts.obtener(instr.id).tipo == instr.expNumerica.tipo and instr.expNumerica.tipo == TS.TIPO_DATO.FLOAT:
                print("son float")
                simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
                ts.actualizar(simbolo)    
            elif ts.obtener(instr.id).tipo ==instr.expNumerica.tipo and instr.expNumerica.tipo == TS.TIPO_DATO.CARACTER:
                print("son char")
                simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
                ts.actualizar(simbolo)  
            elif ts.obtener(instr.id).tipo ==instr.expNumerica.tipo and instr.expNumerica.tipo == TS.TIPO_DATO.CADENA:
                print("son char arreglo")
                simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
                ts.actualizar(simbolo)         
            else:
                print("no son del mismo tipo")
                err = "Error de tipos \'" + str(ts.obtener(instr.id).tipo)+ "\' con \'" +str(instr.expNumerica.tipo)+"\' en la linea: "+str(instr.expNumerica.linea)
                print(err)
                errores.append(err)
        else:
            print("no existe la variable")
            #simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
            #ts.agregar(simbolo)

def procesar_definicion_asignacion(instr,ts):
    val = resolver_expresion_aritmetica(instr.expNumerica, ts)
    print("procesar definicion asignacion :",instr.id,"=",val)
    for i in instr.id:
        if ts.existe(i) :
            print("existe solo se actualiza",ts.obtener(instr.id).tipo,"expresion es tipo:",instr.expNumerica.tipo)
            if ts.obtener(instr.id).tipo == "int" and instr.expNumerica.tipo == TS.TIPO_DATO.NUMERO:
                print("son int")
                simbolo = TS.Simbolo(i.id, instr.expNumerica.tipo, val)
                ts.actualizar(simbolo)
            elif ts.obtener(i.id).tipo == "float" and instr.expNumerica.tipo == TS.TIPO_DATO.FLOAT:
                print("son float")
                simbolo = TS.Simbolo(i.id, instr.expNumerica.tipo, val)
                ts.actualizar(simbolo)    
            elif ts.obtener(i.id).tipo == "char" and instr.expNumerica.tipo == TS.TIPO_DATO.CARACTER:
                print("son char")
                simbolo = TS.Simbolo(input.id, instr.expNumerica.tipo, val)
                ts.actualizar(simbolo)    
            elif ts.obtener(i.id).tipo == "char" and instr.expNumerica.tipo == TS.TIPO_DATO.CADENA:
                print("son char")
                simbolo = TS.Simbolo(input.id, instr.expNumerica.tipo, val)
                ts.actualizar(simbolo)    
            else:
                print("no son del mismo tipo")
                err = "Error de tipos \'" + str(ts.obtener(i.id).tipo)+ "\' con \'" +str(instr.expNumerica.tipo)+"\' en la linea: "+str(instr.expNumerica.linea)
                print(err)
                errores.append(err)

        else:
            print("no existe se guarda en ts",i.id, "tipo :",instr.tipo,"tipo dato: ",instr.expNumerica.tipo)
            if  instr.tipo == "int" and instr.expNumerica.tipo == TS.TIPO_DATO.NUMERO:
                print("es int")
                simbolo = TS.Simbolo(i.id, TS.TIPO_DATO.NUMERO, val)
                ts.agregar(simbolo)
            elif instr.tipo == "float" and instr.expNumerica.tipo == TS.TIPO_DATO.FLOAT:
                print("es float")
                simbolo = TS.Simbolo(i.id, TS.TIPO_DATO.FLOAT, val)
                ts.agregar(simbolo)
            elif instr.tipo == "char" and instr.expNumerica.tipo == TS.TIPO_DATO.CARACTER:
                print("es char")
                simbolo = TS.Simbolo(i.id, TS.TIPO_DATO.CARACTER, val)
                ts.agregar(simbolo)
            elif instr.tipo == "char" and instr.expNumerica.tipo == TS.TIPO_DATO.CADENA:
                print("es char cadena")
                simbolo = TS.Simbolo(i.id, TS.TIPO_DATO.CADENA, val)
                ts.agregar(simbolo)    
            else:
                print("no son del mismo tipo")
                err = "Error de tipos \'" + str(instr.tipo)+ "\' con \'" +str(instr.expNumerica.tipo)+"\' en la linea: "+str(instr.expNumerica.linea)
                print(err)
                errores.append(err)
 
def procesar_asignacion_arreglo(instr,ts):
    ind = resolver_expresion_aritmetica(instr.expNumerica, ts)
    val = resolver_expresion_aritmetica(instr.expNumerica2, ts)
    #print("procesar asignacion en arreglo",instr.id,"indice:",ind,"valor: ", val)
    if ts.existe(instr) :
           # print("existe solo se actualiza", )
            arreglo = ts.obtener(instr.id).valor
            tipo = ts.obtener(instr.id).tipo
            #print("tamaño arreglo: ",len(arreglo))
            if len(arreglo) == 0:
               # print("tamaño es igual a 0")
              #  print("rango:", range(0,ind))
                for x in range(0,ind+1):
                    
                    if x == ind:
                        
                        arreglo.append(0)                
                        arreglo[ind] = val
                        
                    else:
                        
                        arreglo.append(0)
                        
            elif len(arreglo) <= ind:
               # print("indice mayor al tamaño del arreglo")
                new_tam = ind - len(arreglo) 
               # print("indices agregar: ",new_tam+1)
                for x in range(0,new_tam+1):
                    if x == new_tam:
                        
                        arreglo.append(0)                
                        arreglo[ind] = val
                        
                    else:
                        
                        arreglo.append(0)
            elif len(arreglo) > ind:
                arreglo[ind] = val
                
            simbolo = TS.Simbolo(instr.id, ts.obtener(instr.id).tipo, arreglo)
            ts.actualizar(simbolo)
    else:
          #  print("no existe se guarda en ts")
            arreglo = []
            tipo = TS.TIPO_DATO.ARREGLO
           # print("tamaño arreglo: ",len(arreglo))
            if len(arreglo) == 0:
               # print("tamaño es igual a 0")
                #print("rango::", range(0,ind))
                
                for x in range(0,ind+1):
                    #print("estro trae la x:",x)
                    if x == ind:
                        
                        arreglo.append(0)                
                        arreglo[ind] = val
                        
                    else:
                        
                        arreglo.append(0)
                        
            elif len(arreglo) <= ind:
                #print("indice mayor al tamaño del arreglo")
                new_tam = ind - len(arreglo) 
                #print("indices agregar: ",new_tam+1)
                for x in range(0,new_tam+1):
                    if x == new_tam:
                        
                        arreglo.append(0)                
                        arreglo[ind] = val
                        
                    else:
                        
                        arreglo.append(0)
            elif len(arreglo) > ind:
                arreglo[ind] = val
                
            simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.ARREGLO, arreglo)
            ts.agregar(simbolo)

   
def procesar_asignacion_arreglo_mul(instr, ts):
    #print("lista dimensiones:",instr.expNumerica,"expresion:",instr.expNumerica2)
    if ts.existe(instr):
        #print("existe",instr.id)
        #print("esto trae el diccionario de la ts: ",ts.obtener(instr.id).valor)
        diccionario = ts.obtener(instr.id).valor
        contador = 0
        contador_acc = len(instr.expNumerica)
        aux1 = diccionario
        for dim in range(len(instr.expNumerica)):
           # print("entro al for")
            if isinstance(instr.expNumerica[dim],ExpresionIdentificador):
                #print("es identificadorsdfg",ts.obtener(instr.expNumerica[dim].id).valor)
                ind = ts.obtener(instr.expNumerica[dim].id).valor
            else:
                ind = instr.expNumerica[dim].val
           # print("indice",ind)
            if dim == contador_acc-1:
                #print("es el ultimo")
                if isinstance(instr.expNumerica2,ExpresionIdentificador):
                    #print("es identificadorsdfg",ts.obtener(instr.expNumerica[dim].id).valor)
                    aux1[ind] = ts.obtener(instr.expNumerica2.id).valor
                else:
                    aux1[ind] = instr.expNumerica2.val
                #aux1[ind] = instr.expNumerica2.val
            else:
               # print("primer else")
                aux = aux1.get(ind)
                #print("auxiliar",aux)
                if aux == None:
                    aux1[ind]={}
                  #  print("if none",aux1)
                    aux1=aux1.get(ind)
                    #print("auxiliar 1:",aux1)
                else:
                    aux1 = aux1.get(ind)
       #print("print diccionario:",diccionario)
        simbolo = TS.Simbolo(instr.id,ts.obtener(instr.id).tipo,diccionario)
        ts.actualizar(simbolo)
    else:
       # print("no existe se guarda en ts",instr.id)
        tipo = TS.TIPO_DATO.ARREGLO
            
        diccionario = {}
        contador = 0
        contador_acc = len(instr.expNumerica)
        aux1 = diccionario
        for dim in range(len(instr.expNumerica)):
            if isinstance(instr.expNumerica[dim],ExpresionIdentificador):
                #print("es identificadorsdfg",ts.obtener(instr.expNumerica[dim].id).valor)
                ind = ts.obtener(instr.expNumerica[dim].id).valor
            else:
                ind = instr.expNumerica[dim].val
          #  print("indice",ind)
            if dim == contador_acc-1:
              #  print("es el ultimo")
                aux1[ind] = resolver_expresion_aritmetica(instr.expNumerica2,ts)
            else:
               # print("primer else")
                aux = aux1.get(ind)
               # print("auxiliar",aux)
                if aux == None:
                    aux1[ind]={}
                   # print("if none",aux1)
                    aux1=aux1.get(ind)
                   # print("auxiliar 1:",aux1)
                else:
                    aux1 = aux1.get(ind)
        #print("print diccionario:",diccionario)
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.ARREGLO,diccionario)
        ts.agregar(simbolo)
        #print("simbolo",simbolo)



def procesar_if(instr,instrucciones, ts) :
    #print("procesando if exp1:",instr.expNumerica," exp2:", instr.expNumerica2)
    val = resolver_expresion_aritmetica(instr.expNumerica,ts)
    
    if val == 1:
        #print("expresion relacional es 1:")
        #print("ahora el goto",instr.expNumerica2)
        procesar_goto(instr.expNumerica2,instrucciones,ts)
        
        return 1
    else:
        return 0

        
        
def procesar_metodo(instr, ts):
    #print("procesando metodo",instr.id)
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.CADENA, 0)      # inicializamos con 0 como valor por defecto
    ts.agregar(simbolo)

    #ts_local = TS.TablaDeSimbolos(ts.simbolos)
    #procesar_instrucciones(instr.instrucciones, ts_local)
    
def procesar_goto(instr,instrucciones,ts):
    #print("procesando goto",instr.metodo.id)
    #print("instrucciones  globales:",instrucciones)
    instr_restantes = []
    contador = 0
    for instruccion in instrucciones:
        #print("contador instrucciones en goto",contador)
        if isinstance(instruccion, Definicion_Metodo):
            #print("es un metodo:", instruccion.id, " ",instr.metodo.id)
            if instr.metodo.id == instruccion.id:
                instr_restantes = instrucciones[contador+1:]
                #print("instrucciones restantes",instr_restantes)
                
                procesar_instrucciones_metodo(instr_restantes,instrucciones,ts)
                return
                #print("metodo no existe")
        contador +=1
    
    
def resolver_cadena(expCad, ts) :
    if isinstance(expCad, ExpresionConcatenar) :
        exp1 = resolver_cadena(expCad.exp1, ts)
        exp2 = resolver_cadena(expCad.exp2, ts)
        return exp1 + exp2
    elif isinstance(expCad, ExpresionEntero) :
        return expCad.val
    elif isinstance(expCad, ExpresionCadenaNumerico) :
        return str(resolver_expresion_aritmetica(expCad.exp, ts))
    else :
        print('Error: Expresión cadena no válida')


def resolver_expreision_logica(expLog, ts) :
    exp1 = resolver_expresion_aritmetica(expLog.exp1, ts)
    exp2 = resolver_expresion_aritmetica(expLog.exp2, ts)
    if expLog.operador == OPERACION_LOGICA.MAYOR_QUE : return exp1 > exp2
    if expLog.operador == OPERACION_LOGICA.MENOR_QUE : return exp1 < exp2
    if expLog.operador == OPERACION_LOGICA.IGUAL : return exp1 == exp2
    if expLog.operador == OPERACION_LOGICA.DIFERENTE : return exp1 != exp2

def getTemp():
    global cont_t
    temp = "$t"+str(cont_t)
    print("temp:",temp)
    cont_t +=1
    return temp

def resolver_expresion_aritmetica(expNum, ts) :
    #print("esta es la expresion ",expNum)
    errores = g.getErrores()
    global codigo3d
    if isinstance(expNum, ExpresionBinaria) :
        print("resolver expresion binaria: ")
        exp1 = resolver_expresion_aritmetica(expNum.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2, ts)
        print("tipo exp1 :",expNum.exp1.tipo)
        print("tipo exp2 :",expNum.exp2.tipo)
        if expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_ARITMETICA.MAS:
                        
            #expNum.val = exp1 + exp2
            expNum.tipo = expNum.exp1.tipo
            tmp = getTemp()
            codigo3d += tmp + "=" + str(expNum.exp1.val) + "+" + str(expNum.exp2.val)+";\n"
            print(codigo3d)
            return tmp
        
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_ARITMETICA.MENOS:
            expNum.val = exp1 - exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val 
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_ARITMETICA.POR:
            expNum.val = exp1 * exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_ARITMETICA.DIVIDIDO:
            expNum.val = exp1 / exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_ARITMETICA.RESIDUO:
            expNum.val = exp1 % exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif (str(expNum.exp1.tipo) == "TIPO_DATO.FLOAT" and str(expNum.exp2.tipo) == "TIPO_DATO.NUMERO" and expNum.operador == OPERACION_ARITMETICA.RESIDUO) or (str(expNum.exp1.tipo) == "TIPO_DATO.NUMERO" and str(expNum.exp2.tipo) == "TIPO_DATO.FLOAT" and expNum.operador == OPERACION_ARITMETICA.RESIDUO):
            expNum.val = exp1 % exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif str(expNum.exp1.tipo) == "TIPO_DATO.NUMERO" and str(expNum.exp2.tipo) == "TIPO_DATO.CADENA":
                expNum.val = 0
                expNum.tipo = "TIPO_DATO.ERROR"
                #print("error no se puede operar numero con cadena")
                
                err = "Error de tipos \'" + str(expNum.exp1.val)+ "\' con \'" +str(expNum.exp2.val)+"\' en la linea: "+ str(expNum.exp1.linea)
                errores.append(err)
                return expNum.val
        elif str(expNum.exp1.tipo) == "TIPO_DATO.NUMERO" and str(expNum.exp2.tipo) == "TIPO_DATO.CARACTER":
                expNum.val = 0
                expNum.tipo ="TIPO_DATO.ERROR"
                #print("error no se puede operar numero con cadena")
                
                err = "Error de tipos \'" + str(expNum.exp1.val)+ "\' con \'" +str(expNum.exp2.val)+"\' en la linea: "+ str(expNum.exp1.linea)
                errores.append(err)
                return expNum.val
        elif str(expNum.exp1.tipo) == "TIPO_DATO.FLOAT" and str(expNum.exp2.tipo) == "TIPO_DATO.CARACTER":
                expNum.val = 0
                expNum.tipo = "TIPO_DATO.ERROR"
                #print("error no se puede operar numero con cadena")
                
                err = "Error de tipos \'" + str(expNum.exp1.val)+ "\' con \'" +str(expNum.exp2.val)+"\' en la linea: "+ str(expNum.exp1.linea)
                errores.append(err)
                return expNum.val
        elif str(expNum.exp1.tipo) == "TIPO_DATO.FLOAT" and str(expNum.exp2.tipo) == "TIPO_DATO.CADENA":
                expNum.val = 0
                expNum.tipo = "TIPO_DATO.ERROR"
                #print("error no se puede operar numero con cadena")
                
                err = "Error de tipos \'" + str(expNum.exp1.val)+ "\' con \'" +str(expNum.exp2.val)+"\' en la linea: "+ str(expNum.exp1.linea)
                errores.append(err)
                return expNum.val
        elif str(expNum.exp1.tipo) == "TIPO_DATO.CADENA" and str(expNum.exp2.tipo) == "TIPO_DATO.NUMERO":
                expNum.val = 0
                expNum.tipo ="TIPO_DATO.ERROR"
                err = "Error de tipos \'" + str(expNum.exp1.val)+ "\' con \'" +str(expNum.exp2.val)+"\' en la linea: "+ str(expNum.exp1.linea)
                errores.append(err)
                return expNum.val
                #print("error no se puede sumar cadena con numero")
        elif str(expNum.exp1.tipo) == "TIPO_DATO.CADENA" and str(expNum.exp2.tipo) == "TIPO_DATO.FLOAT":
                expNum.val = 0
                expNum.tipo = "TIPO_DATO.ERROR"
                err = "Error de tipos \'" + str(expNum.exp1.val)+ "\' con \'" +str(expNum.exp2.val)+"\' en la linea: "+ str(expNum.exp1.linea)
                errores.append(err)
                return expNum.val
        elif str(expNum.exp1.tipo) == "TIPO_DATO.CARACTER" and str(expNum.exp2.tipo) == "TIPO_DATO.NUMERO":
                expNum.val = 0
                expNum.tipo = "TIPO_DATO.ERROR"
                err = "Error de tipos \'" + str(expNum.exp1.val)+ "\' con \'" +str(expNum.exp2.val)+"\' en la linea: "+ str(expNum.exp1.linea)
                errores.append(err)
                return expNum.val
                #print("error no se puede sumar cadena con numero")
        elif str(expNum.exp1.tipo) == "TIPO_DATO.CARACTER" and str(expNum.exp2.tipo) == "TIPO_DATO.FLOAT":
                expNum.val = 0
                expNum.tipo = "TIPO_DATO.ERROR"
                err = "Error de tipos \'" + str(expNum.exp1.val)+ "\' con \'" +str(expNum.exp2.val)+"\' en la linea: "+ str(expNum.exp1.linea)
                errores.append(err)
                return expNum.val
                #print("error no se puede sumar cadena con numero")        
        #expresion relacionales        
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.IGUAL:
            if exp1 == exp2 :
                #print("expresion relacional es igual ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion relacional no es igual ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.DIFERENTE:
            if exp1 != exp2 :
                #print("expresion relacional es not igual ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion relacional no es not igual ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.MAYORIGUAL:
            if exp1 >= exp2 :
                #print("expresion relacional es mayor igual ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion relacional no es mayor igual ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.MENORIGUAL:
            if exp1 <= exp2 :
                #print("expresion relacional es menor igual ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion relacional no es menor igual ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.MAYOR_QUE:
            if exp1 > exp2 :
                #print("expresion relacional es mayor ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion relacional no es mayor ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.MENOR_QUE:
            if exp1 < exp2 :
                #print("expresion relacional es menor ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion relacional no es menor ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        # expresiones logicas
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.AND:
            if exp1 * exp2 == 1 :
                #print("expresion logica and verdadera ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion logica and falsa ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.OR:
            if exp1 + exp2 >= 1 :
                #print("expresion logica or verdadera ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion logica or falsa ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val 
        # XOR
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.XOR:
            if exp1 + exp2 == 1 :
                #print("expresion logica xor verdadera ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion logica or falsa ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val 
        # LOGICAS BITS
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.ANDBIT:
            #print("expresion logica and bit")
            expNum.val = exp1 & exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.ORBIT:
            #print("expresion logica OR bit")
            expNum.val = exp1 | exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.XORBIT:
            #print("expresion logica XOR bit")
            expNum.val = exp1 ^ exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.MENORBIT:
            #print("expresion logica << bit")
            expNum.val = exp1 << exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.MAYORBIT:
            #print("expresion logica >> bit")
            expNum.val = exp1 >> exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
    elif isinstance(expNum, ExpresionNegativo) :
        expNum.val = resolver_expresion_aritmetica(expNum.val, ts)
        expNum.tipo = expNum.tipo
        return expNum.val * -1
    elif isinstance(expNum, ExpresionEntero) :
        print("expresion entero:", expNum.tipo)
        expNum.val = expNum.val
        expNum.tipo = expNum.tipo
        return expNum.val
    elif isinstance(expNum, ExpresionIdentificador) :
        #print("resolver expresion temporal: ",ts.obtener(expNum.id).valor)
        expNum.val = ts.obtener(expNum.id).valor
        expNum.tipo = ts.obtener(expNum.id).tipo
        return expNum.val
    elif isinstance(expNum, ExpresionAbsoluto):
        #print("resolver expresion absoluto: ",ts.obtener(expNum.id.id).valor)
        expNum.val = ts.obtener(expNum.id.id).valor
        expNum.tipo = ts.obtener(expNum.id.id).tipo
        if expNum.val < 0 :
            return expNum.val * -1
        else:
            return expNum.val
    elif isinstance(expNum, ExpresionConversionInt):
        #print("resolver expresion conversion int: ", ts.obtener(expNum.id.id).tipo)
        if isinstance(ts.obtener(expNum.id.id).valor, float):
            #print("es float")
            expNum.val = int(ts.obtener(expNum.id.id).valor)
            expNum.tipo = TS.TIPO_DATO.NUMERO
        elif ts.obtener(expNum.id.id).tipo == TS.TIPO_DATO.CARACTER:
            #print("es char: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = ord(ts.obtener(expNum.id.id).valor)
            expNum.tipo = TS.TIPO_DATO.NUMERO#ts.obtener(expNum.id.id).tipo
        elif ts.obtener(expNum.id.id).tipo == TS.TIPO_DATO.ARREGLO:
            #print("es ARREGLO: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = ord(ts.obtener(expNum.id.id).valor[0][0])
            expNum.tipo = TS.TIPO_DATO.NUMERO#ts.obtener(expNum.id.id).tipo
        elif isinstance(ts.obtener(expNum.id.id).valor, str):
            #print("es cadena: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = ord(ts.obtener(expNum.id.id).valor[0])
            expNum.tipo = TS.TIPO_DATO.NUMERO#ts.obtener(expNum.id.id).tipo
        
        return expNum.val
    elif isinstance(expNum, ExpresionConversionFloat):
        #print("resolver expresion conversion float: ", ts.obtener(expNum.id.id).valor)
        if isinstance(ts.obtener(expNum.id.id).valor, int):
            #print("es int")
            expNum.val = float(ts.obtener(expNum.id.id).valor)
            expNum.tipo = TS.TIPO_DATO.FLOAT#ts.obtener(expNum.id.id).tipo
        elif ts.obtener(expNum.id.id).tipo == TS.TIPO_DATO.CARACTER:
            #print("es char: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = float(ord(ts.obtener(expNum.id.id).valor))
            expNum.tipo = TS.TIPO_DATO.FLOAT#ts.obtener(expNum.id.id).tipo
        elif ts.obtener(expNum.id.id).tipo == TS.TIPO_DATO.ARREGLO:
            #print("es char: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = float(ord(ts.obtener(expNum.id.id).valor[0][0]))
            expNum.tipo = TS.TIPO_DATO.FLOAT#ts.obtener(expNum.id.id).tipo
        elif isinstance(ts.obtener(expNum.id.id).valor, str):
            #print("es cadena: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = float(ord(ts.obtener(expNum.id.id).valor[0]))
            expNum.tipo = TS.TIPO_DATO.FLOAT#ts.obtener(expNum.id.id).tipo
        return expNum.val
    elif isinstance(expNum, ExpresionConversionChar):
        print("resolver expresion conversion char: ", ts.obtener(expNum.id.id).valor)
        if (isinstance(ts.obtener(expNum.id.id).valor, int) and ts.obtener(expNum.id.id).valor <= 255 ):
            #print("es int y menor a 255")
            expNum.val = chr(ts.obtener(expNum.id.id).valor)
            expNum.tipo = TS.TIPO_DATO.CARACTER#ts.obtener(expNum.id.id).tipo
        elif (isinstance(ts.obtener(expNum.id.id).valor, int) and ts.obtener(expNum.id.id).valor > 255 ):
            #print("es int y mayor a 255")
            expNum.val = chr(ts.obtener(expNum.id.id).valor % 256)
            expNum.tipo = TS.TIPO_DATO.CARACTER#ts.obtener(expNum.id.id).tipo
        elif isinstance(ts.obtener(expNum.id.id).valor, float):
            print("es float")
            expNum.val = int(ts.obtener(expNum.id.id).valor)
            print(expNum.val)
            if expNum.val <= 255:
                expNum.val = chr(expNum.val)
                expNum.tipo = TS.TIPO_DATO.CARACTER#ts.obtener(expNum.id.id).tipo
            else:
                expNum.val = chr(ts.obtener(expNum.id.id).valor % 256)
                expNum.tipo = TS.TIPO_DATO.CARACTER#ts.obtener(expNum.id.id).tipo               
                                
        elif isinstance(ts.obtener(expNum.id.id).valor, str):
            #print("es cadena: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = ts.obtener(expNum.id.id).valor[0]
            expNum.tipo = TS.TIPO_DATO.CARACTER#ts.obtener(expNum.id.id).tipo
            
        elif ts.obtener(expNum.id.id).tipo == TS.TIPO_DATO.ARREGLO:
            #print("es char: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = ts.obtener(expNum.id.id).valor[0][0]
            expNum.tipo = TS.TIPO_DATO.CARACTER#ts.obtener(expNum.id.id).tipo
        return expNum.val 
    elif isinstance(expNum, ExpresionNot):
        #print("resolver expresion not: ", ts.obtener(expNum.id.id).valor)
        if ts.obtener(expNum.id.id).valor == 1:
            expNum.val = 0
            expNum.tipo = ts.obtener(expNum.id.id).tipo
        else:
            expNum.val = 1
            expNum.tipo = ts.obtener(expNum.id.id).tipo
        return expNum.val
    elif isinstance(expNum, ExpresionNotBit):
        #print("resolver expresion not bit: ", ts.obtener(expNum.id.id).valor)
        expNum.val = ~ ts.obtener(expNum.id.id).valor
        expNum.tipo = ts.obtener(expNum.id.id).tipo
        return expNum.val
    elif isinstance(expNum, ExpresionArreglo):
        #print("expresion arreglo:", expNum.tipo)
        expNum.val = {}
        expNum.tipo = expNum.tipo
        return expNum.val
    elif isinstance(expNum, AccesoArreglo):
        #print("expresion acceso arreglo:", expNum.expNumerica)
        aux = ts.obtener(expNum.id).valor
        aux1 = aux
        cantidad_acc = len(expNum.expNumerica)
        #print("aux",aux)
        for i in range(len(expNum.expNumerica)):
            if isinstance(expNum.expNumerica[i],ExpresionIdentificador):
                #print("es exp ident",ts.obtener(expNum.expNumerica[i].id).valor)
                indice = ts.obtener(expNum.expNumerica[i].id).valor
            else:
                
                indice = expNum.expNumerica[i].val
            #print("indice",indice)
            if i == cantidad_acc -1:
                aux1 = aux1.get(indice)
                #print("ultimo",aux1)
            else:
                aux = aux1.get(indice)
                if aux ==None:
                    print("indice no existe")
                else:
                    aux1 = aux1.get(indice)
        #print("esto trae el aux1",aux1)
        expNum.val = aux1
        return expNum.val

def procesar_instrucciones_main_debug(instrucciones,contador,ts):
    #print("entro al debug en pos",contador)
    if instrucciones[0].id == "main":
        
        
        print("instruccion:", instrucciones[contador])            
        if isinstance(instrucciones[contador+1], Imprimir) : 
            
            procesar_imprimir(instrucciones[contador+1],ts)
            
            #hijo = graficar_imprimir(instr,n_print,ts)
        elif isinstance(instrucciones[contador+1], Definicion_Asignacion) : 
            
            procesar_asignacion(instrucciones[contador+1], ts)
            
            #graficar_asignacion(instr,n_asing,ts)    
        elif isinstance(instrucciones[contador+1], Definicion_Asignacion_Arreglo) : 
            
            procesar_asignacion_arreglo(instrucciones[contador+1], ts)    
        elif isinstance(instrucciones[contador+1], Definicion_Asignacion_Arreglo_Multiple) : 
            
            procesar_asignacion_arreglo_mul(instrucciones[contador+1], ts)    
        elif isinstance(instrucciones[contador+1], If) :
            
            
            if procesar_if(instrucciones[contador+1],instrucciones, ts) == 1:
                
                return
        elif isinstance(instrucciones[contador+1], Borrar) : procesar_borrar(instrucciones[contador+1],ts)
        #elif isinstance(instr, Definicion_Metodo) : n_metodo = Node("metodo",parent=n_main)
        elif isinstance(instrucciones[contador+1], Goto) : 
            procesar_goto(instrucciones[contador+1],instrucciones,ts)
            
            return
        elif isinstance(instrucciones[contador+1], Exit) : 
            #print("exit")            
            return             
        else : print('Error: instruccion no valida en main')
    
    else:
        print("metodo principal no esta al inicio o no existe")

def procesar_instrucciones_main( instrucciones, ts):
    #print("procesar main")    
    
    for instr in instrucciones :
        #print("instruccion:", instr)            
        if isinstance(instr, Imprimir) : 
            print("imprimir")
            procesar_imprimir(instr,ts)
            
            #hijo = graficar_imprimir(instr,n_print,ts)
        elif isinstance(instr, Definicion) : 
            print("definicion",instr.tipo, " ",instr.id[0].id)
            procesar_definicion(instr,ts)
        elif isinstance(instr, Asignacion):
            print("asignacion",instr.id, instr.expNumerica.val)
            procesar_asignacion(instr,ts)
        elif isinstance(instr, Definicion_Asignacion) : 
            print("definicion asignacion")
            procesar_definicion_asignacion(instr, ts)
            
            #graficar_asignacion(instr,n_asing,ts)    
        elif isinstance(instr, Definicion_Asignacion_Arreglo) : 
            print("imprimir")
            #procesar_asignacion_arreglo(instr, ts)    
        elif isinstance(instr, Definicion_Asignacion_Arreglo_Multiple) : 
            print("imprimir")
            #procesar_asignacion_arreglo_mul(instr, ts)    
        elif isinstance(instr, If) :
            print("imprimir")
            
            #if procesar_if(instr,instrucciones, ts) == 1:
                
                #return
        
        #elif isinstance(instr, Definicion_Metodo) : n_metodo = Node("metodo",parent=n_main)
            
        else : print('Error: instruccion no valida en main')
    

             
def procesar_instrucciones_metodo(instrucciones,instr_globales, ts) :
    ## lista de instrucciones recolectadas
    #print("procesar metodo")
    #n_metodo=Node("metodo",parent=padre)
    for instr in instrucciones :
        #print("esto trae",instr)
            
        if isinstance(instr, Imprimir) : 
           
            procesar_imprimir(instr, ts)
        elif isinstance(instr, Definicion_Asignacion) : 
            
            procesar_asignacion(instr, ts)  
        elif isinstance(instr, Definicion_Asignacion_Arreglo) : 
            
            procesar_asignacion_arreglo(instr,ts)
        elif isinstance(instr, Definicion_Asignacion_Arreglo_Multiple) : 
                
            procesar_asignacion_arreglo_mul(instr, ts)                
        elif isinstance(instr, If) : 
            
            if procesar_if(instr,instr_globales, ts) == 1:
                return
            
        elif isinstance(instr, Borrar) : procesar_borrar(instr,ts)
        #elif isinstance(instr, Definicion_Metodo) : break
        elif isinstance(instr, Goto) : 
            #print("entro al goto")
            procesar_goto(instr,instr_globales,ts)
            return
        elif isinstance(instr, Exit) : 
            #print("exit")            
            break                      
        else : print('Error: instruccion no valida metodo')

def graficar_arbol(instrucciones):
    raiz = Node("root")
    metodo = raiz
    contador = 0
    instr_restantes = []
    for instr in instrucciones :
        
            
        if isinstance(instr, Imprimir) : 
            n_print= Node("imprimir", parent=raiz)
            #hijo = Node(instr.cad,parent=n_print)
        
        elif isinstance(instr, Definicion_Asignacion) : 
            n_asing= Node("asignar", parent=raiz)
            #graficar_hijos(instr,n_asing)
        elif isinstance(instr, Definicion_Asignacion_Arreglo) : 
            n_arr = Node("asignar arreglo", parent=raiz)
            
        elif isinstance(instr, Definicion_Asignacion_Arreglo_Multiple) : 
            n_arr_m = Node("asignar arreglo multiple",parent=raiz)    
        elif isinstance(instr, If) : 
            n_if = Node("if",parent=raiz)
                        
        elif isinstance(instr, Borrar) : 
            n_borrar = Node("borrar",parent=raiz)
            
        elif isinstance(instr, Definicion_Metodo) :             
            n_metodo = Node("metodo",parent=raiz)
            instr_restantes = []
            contador = 0
            for instruccion in instrucciones:
                #print("contador instrucciones en goto",contador)
                if isinstance(instruccion, Definicion_Metodo):
                    #print("es un metodo:", instruccion.id, " ",instr.metodo.id)
                    if instr.id == instruccion.id:
                        instr_restantes = instrucciones[contador+1:]
                        #print("instrucciones restantes",instr_restantes)
                        graficar_hijos(instr_restantes,n_metodo)
                        UniqueDotExporter(raiz).to_picture("ast.png") 
                        return
                        #print("metodo no existe")
                contador +=1
            
            
        elif isinstance(instr, Goto) : 
            #print("entro al goto")
            n_goto = Node("goto",parent=raiz)

        elif isinstance(instr, Exit) : 
            #print("exit")            
            n_exit = Node("exit",parent=raiz)
        else : print('Error: instruccion no valida graficar')
        
    UniqueDotExporter(raiz).to_picture("ast.png") 

def graficar_hijos(instrucciones,raiz):
    for instr in instrucciones :
        #print("instruccion:", instr)  
        if isinstance(instr, Imprimir) : 
            n_print= Node("imprimir", parent=raiz)
            #hijo = Node(instr.cad,parent=n_print)
        
        elif isinstance(instr, Definicion_Asignacion) : 
            n_asing= Node("asignar", parent=raiz)
            
        elif isinstance(instr, Definicion_Asignacion_Arreglo) : 
            n_arr = Node("asignar arreglo", parent=raiz)
            
        elif isinstance(instr, Definicion_Asignacion_Arreglo_Multiple) : 
            n_arr_m = Node("asignar arreglo multiple",parent=raiz)

        elif isinstance(instr, If) : 
            n_if = Node("if",parent=raiz)
                        
        elif isinstance(instr, Borrar) : 
            n_borrar = Node("borrar",parent=raiz)
            
        elif isinstance(instr, Definicion_Metodo) : 
            n_metodo = Node("metodo",parent=raiz)
            instr_restantes = []
            contador = 0
            for instruccion in instrucciones:
                #print("contador instrucciones en goto",contador)
                if isinstance(instruccion, Definicion_Metodo):
                    #print("es un metodo:", instruccion.id, " ",instr.metodo.id)
                    if instr.id == instruccion.id:
                        instr_restantes = instrucciones[contador+1:]
                        #print("instrucciones restantes",instr_restantes)
                        graficar_hijos(instr_restantes,n_metodo)
                        return
                        #print("metodo no existe")
                contador +=1    

            graficar_hijos(instr.id,n_metodo)
            
        elif isinstance(instr, Goto) : 
            #print("entro al goto")
            n_goto = Node("goto",parent=raiz)
        elif isinstance(instr, Exit) : 
            #print("exit")            
            n_exit = Node("exit",parent=raiz)
        else : print('Error: instruccion no valida graficar hijo')

def reporte_errores(errores):
    open('errores','w').close()
    if errores == None:
        print("no hay errores")
        return
    else:
        d = Digraph('G', filename='errores')
        cont=0
        nodo = ""
        
        for err in errores:
            #print("esto trae:",err)
            nodo += '<TR><TD>'+err+'</TD></TR>'
            
        #print("nodo",nodo)    
        d.node('tab',label='''<<TABLE>
        '''+nodo+'''
        </TABLE>>''')
        d.view()

def reporte_gramatica(gramatica):
    #print("reporte gramatica",gramatica)
    
    d = Digraph('G', filename='gramatical')
    cont=0
    nodo = ""
    nueva = gramatica[::-1]
    #rint("nueva",nueva)
    for gram in nueva:
        print("esto trae:",gram)
        nodo += '<TR><TD>'+gram+'</TD></TR>'
        
    print("nodo",nodo)    
    d.node('tab2',label='''<<TABLE>
    '''+nodo+'''
    </TABLE>>''')
    d.view()

def reporte_tabla_simbolos(simbolos):
    print("reporte ts")
    d = Digraph('G', filename='simbolos')
    cont=0
    nodo = ""
    for simbolo in simbolos:
        print("esto trae:",simbolos[simbolo].id,"tipo: ",simbolos[simbolo].id,"valor ",simbolos[simbolo].valor)
        nodo += '<TR><TD>'+simbolos[simbolo].id+'</TD><TD>'+str(simbolos[simbolo].tipo)+'</TD><TD>'+str(simbolos[simbolo].valor)+'</TD></TR>'
        
    #print("nodo",nodo)    
    d.node('tab3',label='''<<TABLE>
    '''+nodo+'''
    </TABLE>>''')
    d.view()

    
#reporte_errores()   

f = open("./entrada2.txt", "r")
input = f.read()

instrucciones = g.parse(input)
errores = g.getErrores()
print("eso trae la lista_errores", errores)           

print("primer print:",instrucciones)
ts_global = TS.TablaDeSimbolos()
#graficar_arbol(instrucciones)
procesar_instrucciones_main(instrucciones, ts_global)
#generar_arbol(instrucciones,ts_global)
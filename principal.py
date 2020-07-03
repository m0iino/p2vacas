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
cont_p=0
cont_re=0
cont_pila=0
codigo3d = ""
codigog = ""
etiquetas = ""
cont_v=0
cont_e=0
cont_ef=0
cont_c = 0
cont_s=0
cont_b=0
cont_salida = 0
cont_global=0
cont_w=0
cont_dw=0
cont_f=0
def procesar_imprimir(instr, ts) :
    global cadena,codigo3d
    print("instruccion:",instr.cad)
    val = resolver_expresion_aritmetica(instr.cad, ts)
    codigo3d += "print("+str(val)+");\n"
    #print(codigo3d)
    cadena = cadena+'> ' + str(val) +'\n'
    #print(cadena)
def procesar_imprimir_compuesto(instr, ts) :
    global cadena,codigo3d
    print("instruccion:",instr.cad.val)
    print("ids",instr.ids)
    temporales=[]
    tipo=[]
    cont_pos1=0
    cont_pos2=0
    if isinstance(instr.ids[0],ExpresionBinaria):
        print("print es binaria")
        val = resolver_expresion_aritmetica(instr.ids[0],ts)
        print(val)
        codigo3d += "print(\""+str(instr.cad.val)+"\");\n"
        codigo3d += "print("+str(val)+");\n"
    else:

        for index in range(len(instr.cad.val)):
            #print("esto trae",instr.cad.val[index])
            if (instr.cad.val[index] == '%') and (instr.cad.val[index+1] == 'd'):
                print("es %"+"d")
                tipo.append("double")
                cont_pos1 += 1
            elif (instr.cad.val[index] == '%') and (instr.cad.val[index+1] == 'c'):
                print("es %"+"c")
                tipo.append("char")
                cont_pos1 += 1
            elif (instr.cad.val[index] == '%') and (instr.cad.val[index+1] == 'f'):
                print("es %"+"f")
                tipo.append("float")
                cont_pos1 += 1
            elif (instr.cad.val[index] == '%') and (instr.cad.val[index+1] == 's'):
                print("es %"+"s")
                tipo.append("string")
                cont_pos1 += 1
            elif (instr.cad.val[index] == '%') and (instr.cad.val[index+1] == 'i'):
                print("es %"+"i")
                tipo.append("arreglo")
                cont_pos1 += 1
        for identi in instr.ids:
            print(identi.id)
            simbolo = ts.obtener(identi.id)
            print(simbolo.temporal)
            temporales.append(simbolo)
            cont_pos2 += 1
        
        if cont_pos1 == cont_pos2:
            cont =0
            print("son iguales")
            print(instr.cad.val.split('%'))
            for i in instr.cad.val.split('%'):
                #print("for",i)
                if not i:
                    print("vacio")
                else:
                    print("tipo:",temporales[cont].tipo,temporales[cont].temporal,temporales[cont].id)
                    if i[0] == 'd' :
                        #print("es %"+"d")
                        codigo3d += "print("+str(temporales[cont].temporal)+");\n"
                        cont +=1
                    elif i[0] == 'c':
                        #print("es %"+"c")
                        codigo3d += "print("+str(temporales[cont].temporal)+");\n"
                        cont +=1
                    elif i[0]== 'f':
                        #print("es %"+"f")
                        codigo3d += "print("+str(temporales[cont].temporal)+");\n"
                        cont +=1                
                    elif i[0] == 's':
                        #print("es %"+"s")
                        codigo3d += "print("+str(temporales[cont].temporal)+");\n"
                        cont +=1
                    else:
                        codigo3d += "print('"+str(i)+"');\n"

        else:
            print("cantidad de valores no son iguales")
    
    #val = resolver_expresion_aritmetica(instr.cad, ts)
    #codigo3d += "print("+str(val)+");\n"
    #print(codigo3d)
    #cadena = cadena+'> ' + str(val) +'\n'
    #print(cadena)
def getCadena():
    global codigo3d
    #print("get cadena:",cadena)
    return codigo3d
    
def procesar_borrar(instr,ts):
    #print("procesar borrar: ")
    ts.borrar(instr.cad.id)
    

def procesar_definicion(instr,ambito, ts) :
    global cont_v
    global codigo3d
    if isinstance(instr, Definicion_Asignacion_Arreglo_Multiple):
        print("definicion arreglo")
        tmp = getTemp()
        simbolo = TS.Simbolo(instr.id, instr.tipo, [],cont_v,ambito,TS.TIPO_DATO.VARIABLE,tmp)
        cont_v += 1
        ts.agregar(simbolo)
        codigo3d += str(tmp)+"= array();\n"
    else:

        print("tamaño:",len(instr.id))
        cont = 0
        for i in instr.id:
            print("id:",i.id)
            cont += 1
            print("procesar definicion: ",i.id,instr.tipo)
            tmp = getTemp()
            simbolo = TS.Simbolo(i.id, instr.tipo, 0,cont_v,ambito,TS.TIPO_DATO.VARIABLE,tmp)
            print("id:",simbolo.id,"tipo:",simbolo.tipo,"direccion:",cont_v,"ambito: ",simbolo.ambito,"rol: ",simbolo.rol,"temp: ",tmp)      # inicializamos con 0 como valor por defecto
            ts.agregar(simbolo)
            print("contador temp: ",cont_v)
            #codigo3d += tmp + "=" + "$sp" "+" + str(cont_v)+";\n"
            cont_v += 1

    print("definicion procesada")
    

def procesar_asignacion(instr,ts) :
    global codigo3d
    val = resolver_expresion_aritmetica(instr.expNumerica, ts)
    print("procesar asignacion :",instr.id,"=",val)
    if isinstance(instr.expNumerica, AccesoArreglo):
        #print("es arreglo")
        if ts.existe(instr) :
            print("existe solo se actualiza",ts.obtener(instr.id).tipo,"expresion es tipo:",instr.expNumerica.tipo)
            if ts.obtener(instr.id).tipo ==  instr.expNumerica.tipo:
                print("son int")
                simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                ts.actualizar(simbolo)
                codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"
            elif ts.obtener(instr.id).tipo == instr.expNumerica.tipo:
                print("son float")
                simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                ts.actualizar(simbolo)
                codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(ival) +";\n"    
            elif ts.obtener(instr.id).tipo ==instr.expNumerica.tipo :
                print("son char")
                simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                ts.actualizar(simbolo)
                codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"  
            elif ts.obtener(instr.id).tipo == "TIPO_DATO.CARACTER" and instr.expNumerica.tipo == TS.TIPO_DATO.CADENA:
                print("son char arreglo")
                simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                ts.actualizar(simbolo)
                codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"    
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
        print("else instr",instr.id)
        if ts.existe(instr) :

            print("existe solo se actualiza asdf",ts.obtener(instr.id),"expresion es tipo:",val)
            print(ts.obtener(instr.id).tipo)
            print(instr.expNumerica.tipo)
            print(instr.expNumerica)
            if isinstance(instr.expNumerica , ExpresionBinaria):
                print("es suma")
                print("tipo",instr.expNumerica.tipo)
                if instr.expNumerica.tipo == TS.TIPO_DATO.NUMERO:
                    print("son int",instr)
                    simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"
                    return str(ts.obtener(instr.id).temporal)
                elif instr.expNumerica.tipo == TS.TIPO_DATO.FLOAT:
                    print("son float")
                    simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"    
                    return str(ts.obtener(instr.id).temporal)
                elif instr.expNumerica.tipo == "double":
                    print("son double")
                    simbolo = TS.Simbolo(instr.id, str(ts.obtener(instr.id).tipo), val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"    
                    return str(ts.obtener(instr.id).temporal)
                elif instr.expNumerica.tipo == "int":
                    print("es int")
                    simbolo = TS.Simbolo(instr.id, str(ts.obtener(instr.id).tipo), val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"    
                    return str(ts.obtener(instr.id).temporal)                             
                elif instr.expNumerica.tipo == TS.TIPO_DATO.CARACTER:
                    print("son char")
                    simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)  
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"
                    return str(ts.obtener(instr.id).temporal)
                elif instr.expNumerica.tipo == TS.TIPO_DATO.CADENA:
                    print("son char arreglo")
                    simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)         
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"
                    return str(ts.obtener(instr.id).temporal)
                else:
                    print("no son del mismo tipo")
                    err = "Error de tipos \'" + str(ts.obtener(instr.id).tipo)+ "\' con \'" +str(instr.expNumerica.tipo)+"\' en la linea: "+str(instr.expNumerica.linea)
                    print(err)
                    errores.append(err)
            elif isinstance(instr.expNumerica,ExpresionEntero):#es expNumerica
                if instr.expNumerica.tipo == TS.TIPO_DATO.NUMERO:
                    print("son int",instr)
                    simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"
                    return str(ts.obtener(instr.id).temporal)
                elif instr.expNumerica.tipo == TS.TIPO_DATO.FLOAT:
                    print("son float")
                    simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"    
                    return str(ts.obtener(instr.id).temporal)
                elif str(ts.obtener(instr.id).tipo) == "double":
                    print("son double")
                    simbolo = TS.Simbolo(instr.id, str(ts.obtener(instr.id).tipo), val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"    
                    return str(ts.obtener(instr.id).temporal)                    
                elif instr.expNumerica.tipo == TS.TIPO_DATO.CARACTER:
                    print("son char")
                    simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo,val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)  
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"
                    return str(ts.obtener(instr.id).temporal)
                elif instr.expNumerica.tipo == TS.TIPO_DATO.CADENA:
                    print("son char arreglo")
                    simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)         
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"
                    return str(ts.obtener(instr.id).temporal)
                else:
                    print("no son del mismo tipo")
                    err = "Error de tipos \'" + str(ts.obtener(instr.id).tipo)+ "\' con \'" +str(instr.expNumerica.tipo)+"\' en la linea: "+str(instr.expNumerica.linea)
                    print(err)
                    errores.append(err)
            else:
                print("no es binaria ni expentero")
                if ts.obtener(instr.id).tipo == "int" and instr.expNumerica.tipo == TS.TIPO_DATO.NUMERO:
                    print("son int",instr)
                    simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"
                    return str(ts.obtener(instr.id).temporal)
                elif ts.obtener(instr.id).tipo == "float" and  instr.expNumerica.tipo == TS.TIPO_DATO.FLOAT:
                    print("son float")
                    simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"  
                    return str(ts.obtener(instr.id).temporal)  
                elif str(ts.obtener(instr.id).tipo) == "double":
                    print("son double")
                    simbolo = TS.Simbolo(instr.id, str(ts.obtener(instr.id).tipo), val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"    
                    return str(ts.obtener(instr.id).temporal)                    
                
                elif ts.obtener(instr.id).tipo == "char" and instr.expNumerica.tipo == TS.TIPO_DATO.CARACTER:
                    print("son char")
                    simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)  
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"
                    return str(ts.obtener(instr.id).temporal)
                elif ts.obtener(instr.id).tipo == "char" and instr.expNumerica.tipo == TS.TIPO_DATO.CADENA:
                    print("son char arreglo")
                    simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val,ts.obtener(instr.id).direccion,ts.obtener(instr.id).ambito,ts.obtener(instr.id).rol,ts.obtener(instr.id).temporal)
                    ts.actualizar(simbolo)         
                    #tmp = getTemp()
                    codigo3d += str(ts.obtener(instr.id).temporal)+ "=" + str(val) +";\n"
                else:
                    print("no son del mismo tipo")
                    err = "Error de tipos \'" + str(ts.obtener(instr.id).tipo)+ "\' con \'" +str(instr.expNumerica.tipo)+"\' en la linea: "+str(instr.expNumerica.linea)
                    print(err)
                    errores.append(err)    
        else:
            print("no existe la variable")
            #simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
            #ts.agregar(simbolo)

def procesar_definicion_asignacion(instr,ambito,ts):
    global cont_v, codigo3d
    print(instr)
    print("tipo:",instr.tipo,"id:",instr.id,"expnumerica:",instr.expNumerica)
    val = resolver_expresion_aritmetica(instr.expNumerica, ts)
    print("procesar definicion asignacion :",instr.id,"=",val)
    for i in instr.id:
        print("entro al for",i)
        if ts.existe(i) :
            print("existe")
            print("existe solo se actualiza",ts.obtener(i.id).tipo,"expresion es tipo:",instr.expNumerica.tipo)
            if ts.obtener(i.id).tipo == TS.TIPO_DATO.NUMERO and instr.expNumerica.tipo == TS.TIPO_DATO.NUMERO:
                print("son int")
                simbolo = TS.Simbolo(i.id, instr.expNumerica.tipo, val,ts.obtener(i.id).direccion,ts.obtener(i.id).ambito,ts.obtener(i.id).rol,ts.obtener(i.id).temporal)
                ts.actualizar(simbolo)
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n"
                
            elif ts.obtener(i.id).tipo == TS.TIPO_DATO.FLOAT and instr.expNumerica.tipo == TS.TIPO_DATO.NUMERO:
                print("son int")
                simbolo = TS.Simbolo(i.id, instr.expNumerica.tipo, val,ts.obtener(i.id).direccion,ts.obtener(i.id).ambito,ts.obtener(i.id).rol,ts.obtener(i.id).temporal)
                ts.actualizar(simbolo)
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n"
            elif ts.obtener(i.id).tipo == TS.TIPO_DATO.NUMERO and instr.expNumerica.tipo == TS.TIPO_DATO.FLOAT:
                print("son int")
                simbolo = TS.Simbolo(i.id, instr.expNumerica.tipo, val,ts.obtener(i.id).direccion,ts.obtener(i.id).ambito,ts.obtener(i.id).rol,ts.obtener(i.id).temporal)
                ts.actualizar(simbolo)
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n"
            elif ts.obtener(i.id).tipo == TS.TIPO_DATO.NUMERO and str(instr.expNumerica) == "scanf":
                print("es scanf")

            elif ts.obtener(i.id).tipo == TS.TIPO_DATO.FLOAT and instr.expNumerica.tipo == TS.TIPO_DATO.FLOAT:
                print("son float")
                simbolo = TS.Simbolo(i.id, instr.expNumerica.tipo, val,ts.obtener(i.id).direccion,ts.obtener(i.id).ambito,ts.obtener(i.id).rol,ts.obtener(i.id).temporal)
                ts.actualizar(simbolo)
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n"    
            
            elif ts.obtener(i.id).tipo == "double" and instr.expNumerica.tipo == TS.TIPO_DATO.FLOAT:
                print("son double")
                simbolo = TS.Simbolo(i.id, instr.expNumerica.tipo, val,ts.obtener(i.id).direccion,ts.obtener(i.id).ambito,ts.obtener(i.id).rol,ts.obtener(i.id).temporal)
                ts.actualizar(simbolo)
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n"    
            
            elif ts.obtener(i.id).tipo == "double" and instr.expNumerica.tipo == TS.TIPO_DATO.NUMERO:
                print("son double")
                simbolo = TS.Simbolo(i.id, instr.expNumerica.tipo, val,ts.obtener(i.id).direccion,ts.obtener(i.id).ambito,ts.obtener(i.id).rol,ts.obtener(i.id).temporal)
                ts.actualizar(simbolo)
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n"    
            
            elif ts.obtener(i.id).tipo == TS.TIPO_DATO.CARACTER and instr.expNumerica.tipo == TS.TIPO_DATO.CARACTER:
                print("son char")
                simbolo = TS.Simbolo(i.id, instr.expNumerica.tipo, val,ts.obtener(i.id).direccion,ts.obtener(i.id).ambito,ts.obtener(i.id).rol,ts.obtener(i.id).temporal)
                ts.actualizar(simbolo) 
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n"   
            elif ts.obtener(i.id).tipo == TS.TIPO_DATO.CARACTER and instr.expNumerica.tipo == TS.TIPO_DATO.CADENA:
                print("son char")
                simbolo = TS.Simbolo(i.id, instr.expNumerica.tipo, val,ts.obtener(i.id).direccion,ts.obtener(i.id).ambito,ts.obtener(i.id).rol,ts.obtener(i.id).temporal)
                ts.actualizar(simbolo) 
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n"   
            else:
                print("no son del mismo tipo")
                err = "Error de tipos \'" + str(ts.obtener(i.id).tipo)+ "\' con \'" +str(instr.expNumerica.tipo)+"\' en la linea: "+str(instr.expNumerica.linea)
                print(err)
                errores.append(err)

        else:
            
            print("no existe se guarda en ts",i.id, "tipo :",instr.tipo,"tipo dato: ",instr.expNumerica.tipo)
            if  instr.tipo == "int" and instr.expNumerica.tipo == TS.TIPO_DATO.NUMERO:
                print("es int")
                tmp = getTemp()
                simbolo = TS.Simbolo(i.id, TS.TIPO_DATO.NUMERO, val,cont_v,ambito,TS.TIPO_DATO.VARIABLE,tmp)
                print("id:",simbolo.id,"tipo:",simbolo.tipo,"valor:",val,"direccion:",cont_v,"ambito: ",simbolo.ambito,"rol: ",simbolo.rol,"temp: ",tmp)      # inicializamos con 0 como valor por defecto
                ts.agregar(simbolo)
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n"
            elif instr.tipo == "float" and instr.expNumerica.tipo == TS.TIPO_DATO.FLOAT:
                print("es float")
                tmp = getTemp()
                simbolo = TS.Simbolo(i.id, TS.TIPO_DATO.FLOAT, val,cont_v,ambito,TS.TIPO_DATO.VARIABLE,tmp)
                print("id:",simbolo.id,"tipo:",simbolo.tipo,"direccion:",cont_v,"ambito: ",simbolo.ambito,"rol: ",simbolo.rol,"temp: ",tmp)      # inicializamos con 0 como valor por defecto
                ts.agregar(simbolo)
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n"
            
            elif instr.tipo == "double" and instr.expNumerica.tipo == TS.TIPO_DATO.FLOAT:
                print("es double")
                tmp = getTemp()
                simbolo = TS.Simbolo(i.id, TS.TIPO_DATO.FLOAT, val,cont_v,ambito,TS.TIPO_DATO.VARIABLE,tmp)
                print("id:",simbolo.id,"tipo:",simbolo.tipo,"direccion:",cont_v,"ambito: ",simbolo.ambito,"rol: ",simbolo.rol,"temp: ",tmp)      # inicializamos con 0 como valor por defecto
                ts.agregar(simbolo)
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n"
            
            elif instr.tipo == "double" and instr.expNumerica.tipo == TS.TIPO_DATO.NUMERO:
                print("es double")
                tmp = getTemp()
                simbolo = TS.Simbolo(i.id, TS.TIPO_DATO.FLOAT, val,cont_v,ambito,TS.TIPO_DATO.VARIABLE,tmp)
                print("id:",simbolo.id,"tipo:",simbolo.tipo,"direccion:",cont_v,"ambito: ",simbolo.ambito,"rol: ",simbolo.rol,"temp: ",tmp)      # inicializamos con 0 como valor por defecto
                ts.agregar(simbolo)
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n"
            elif instr.tipo == "double" and instr.expNumerica.tipo == "int":
                print("es double")
                tmp = getTemp()
                simbolo = TS.Simbolo(i.id, TS.TIPO_DATO.FLOAT, val,cont_v,ambito,TS.TIPO_DATO.VARIABLE,tmp)
                print("id:",simbolo.id,"tipo:",simbolo.tipo,"direccion:",cont_v,"ambito: ",simbolo.ambito,"rol: ",simbolo.rol,"temp: ",tmp)      # inicializamos con 0 como valor por defecto
                ts.agregar(simbolo)
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n"
            elif instr.tipo == "char" and instr.expNumerica.tipo == TS.TIPO_DATO.CARACTER:
                print("es char")
                tmp = getTemp()
                simbolo = TS.Simbolo(i.id, TS.TIPO_DATO.CARACTER, val,cont_v,ambito,TS.TIPO_DATO.VARIABLE,tmp)
                print("id:",simbolo.id,"tipo:",simbolo.tipo,"direccion:",cont_v,"ambito: ",simbolo.ambito,"rol: ",simbolo.rol,"temp: ",tmp)      # inicializamos con 0 como valor por defecto
                ts.agregar(simbolo)
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n"
            elif instr.tipo == "char" and instr.expNumerica.tipo == TS.TIPO_DATO.CADENA:
                print("es char cadena")
                tmp = getTemp()
                simbolo = TS.Simbolo(i.id, TS.TIPO_DATO.CADENA, val,cont_v,ambito,TS.TIPO_DATO.VARIABLE,tmp)
                print("id:",simbolo.id,"tipo:",simbolo.tipo,"direccion:",cont_v,"ambito: ",simbolo.ambito,"rol: ",simbolo.rol,"temp: ",tmp)      # inicializamos con 0 como valor por defecto
                ts.agregar(simbolo) 
                codigo3d += str(ts.obtener(i.id).temporal)+ "=" + str(val) +";\n" 
            else:
                print("no son del mismo tipo")
                err = "Error de tipos \'" + str(instr.tipo)+ "\' con \'" +str(instr.expNumerica.tipo)+"\' en la linea: "+str(instr.expNumerica.linea)
                print(err)
                errores.append(err)



    
        cont_v += 1
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

   
def procesar_asignacion_arreglo_mul(instr,ambito, ts):
    global codigo3d
    print(instr)
    procesar_definicion(instr,ambito,ts)
    print("lista dimensiones:",instr.expNumerica,"expresion:",instr.expNumerica2)
    if ts.existe(instr):
        print("existe",instr.id)
        print("esto trae el diccionario de la ts: ",ts.obtener(instr.id).valor)
        diccionario = ts.obtener(instr.id).valor
        contador = 0
        contador_acc = len(instr.expNumerica)
        aux1 = diccionario
        for i in instr.expNumerica2:
            print("entro al for")
            val = resolver_expresion_aritmetica(i,ts)
            print(val)
            codigo3d += str(ts.obtener(instr.id).temporal)+"["+str(contador)+"] = "+str(val)+";\n"
            contador += 1
       #print("print diccionario:",diccionario)
        #simbolo = TS.Simbolo(instr.id,ts.obtener(instr.id).tipo,diccionario)
        #ts.actualizar(simbolo)
    else:
        print("no existe se guarda en ts",instr.id)
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
                ind = instr.expNumerica.val
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

        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO, diccionario,cont_v,ambito,TS.TIPO_DATO.VARIABLE,tmp)
        #simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.ARREGLO,diccionario)
        ts.agregar(simbolo)
        #print("simbolo",simbolo)

def procesar_llamada_funcion(instr,ambito,ts):
    global codigo3d
    print("procesando llamada", instr.id," parametros:",instr.ids)
    print(len(instr.ids))
    param =[]
    if ts.existeId(instr.id):
        param = ts.obtener(instr.id).valor
    
    print(param)
    cont=0
    if len(param) == len(instr.ids):
        for p in param:
            val = resolver_expresion_aritmetica(instr.ids[cont],ts)
            codigo3d += str(p)+"="+str(val)+";\n"
            cont += 1

    lbls = getSalida()
    codigo3d += "goto " + str(instr.id) + ";\n"
    
    return lbls

def procesar_if(instr, ts) :
    global codigo3d
    print("procesando if exp1:",instr.expNumerica," lista:", instr.instrucciones)
    val = resolver_expresion_aritmetica(instr.expNumerica,ts)
    tmp = getTemp()
    lbl = getEtiquetaVerdadera()
    lblf = getEtiquetaFalsa()
    lbls = getSalida()
    codigo3d += tmp + "=" + str(val) + ";\n"
    codigo3d +="if(" + str(tmp) + ")" + "goto "+str(lbl) +";\n"
    codigo3d +="goto "+str(lblf)+ ";\n"
    codigo3d += str(lbl)+":\n"
    procesar_instrucciones_metodo(instr.instrucciones,"if",ts)
    codigo3d += "goto "+str(lbls)+";\n"
    codigo3d +=str(lblf)+":\n"
    return lbls

def procesar_if_else(instr,ts):
    global codigo3d
    print("procesando if else exp1:",instr.expNumerica," lista verdera:", instr.instrIfVerdadero,"lista falfa: ",instr.instrIfFalso)
    val = resolver_expresion_aritmetica(instr.expNumerica,ts)
    tmp = getTemp()
    lbl = getEtiquetaVerdadera()
    lblf = getEtiquetaFalsa()
    lbls = getSalida()
    codigo3d += tmp + "=" + str(val) + ";\n"
    codigo3d +="if(" + str(tmp) + ")" + "goto "+str(lbl) +";\n"
    codigo3d +="goto "+str(lblf) +";\n"
    print("generar instr verdaderas")
    codigo3d +=str(lbl)+":\n"
    procesar_instrucciones_metodo(instr.instrIfVerdadero,"ifelse",ts)
    codigo3d += "goto "+str(lbls)+";\n"
    codigo3d +=str(lblf)+":\n"
    procesar_instrucciones_metodo(instr.instrIfFalso,"ifelse",ts)
    #lbls = getSalida()
    #codigo3d +="goto"+str(lbls)+";\n"
    print("generar instr falsas")
    return lbls
    #print("generar salida")
    #procesar_instrucciones_metodo([],lbls,ts)

def procesar_if_else_if(instr,ts):
    global codigo3d
    print("procesando if else exp1:",instr.expNumerica," lista verdera:", instr.instrIfVerdadero,"else if: ",instr.expNumerica2)
    val = resolver_expresion_aritmetica(instr.expNumerica,ts)
    tmp = getTemp()
    lbl = getEtiquetaVerdadera()
    lblf = getEtiquetaFalsa()
    lbls = getSalida()
    codigo3d += tmp + "=" + str(val) + ";\n"
    codigo3d +="if(" + str(tmp) + ")" + "goto "+str(lbl) +";\n"
    codigo3d +="goto "+str(lblf) +";\n"
    print("generar instr verdaderas")
    codigo3d +=str(lbl)+":\n"
    procesar_instrucciones_metodo(instr.instrIfVerdadero,"ifelse",ts)
    codigo3d += "goto "+str(lbls)+";\n"
    codigo3d +=str(lblf)+":\n"
    if isinstance(instr.expNumerica2, If):
        i = procesar_if(instr.expNumerica2, ts)
        print("regreso del if",i)
        if i != None:
            print("no es none")
            codigo3d += str(i)+":\n"
    elif isinstance(instr.expNumerica2, IfElse):
        s = procesar_if_else(instr.expNumerica2, ts)
        print("regreso del if",s)
        if s != None:
            print("no es none")
            codigo3d += str(s)+":\n"
    elif isinstance(instr.expNumerica2, IfElseIf):
        ie = procesar_if_else_if(instr.expNumerica2, ts)
        print("regreso del if else if",ie)
        if ie != None:
            print("no es none")
            codigo3d += str(ie)+":\n"
    #procesar_instrucciones_metodo(instr.expNumerica2,"ifelse",ts)
    #lbls = getSalida()
    #codigo3d +="goto"+str(lbls)+";\n"
    print("generar instr falsas")
    return lbls
    #print("generar salida")
    #procesar_instrucciones_metodo([],lbls,ts)
def procesar_return(instr,ts):
    val = resolver_expresion_aritmetica(instr.expNumerica,ts)
    return val
        
def procesar_switch(instr,ts):
    print("procesando switch")
    global codigo3d
    print("procesando switch condicion:",instr.expNumerica," casos:", instr.casos)
    val = resolver_expresion_aritmetica(instr.expNumerica,ts)
    tmp = getTemp()
    
    sw = getEtiquetaSwitch()
    br = getBreak()
    #codigo3d += str(sw)+":\n"
    codigo3d += tmp + "=" + str(val) + ";\n"
    procesar_caso(instr.casos,tmp,br,ts)
    return br
    #codigo3d += str(br)+":\n"


def procesar_caso(instr,tmp,br,ts):
    global codigo3d
    #c = getEtiquetaCaso()
    cont = 0
    
    for caso in instr:
        if isinstance(caso,Default):
            codigo3d += str(c) +":\n"
            #print("procesando caso",caso.expNumerica)
            #val = resolver_expresion_aritmetica(caso.expNumerica,ts)
            c = getEtiquetaCaso()
            procesar_instrucciones_metodo(caso.instrucciones,"switch",ts)
            codigo3d += "goto "+str(br)+";\n"
        elif cont == 0:

            print("procesando caso",caso.expNumerica)
            val = resolver_expresion_aritmetica(caso.expNumerica,ts)
            c = getEtiquetaCaso()
            codigo3d += "if("+str(tmp) +" != "+str(val)+") goto "+str(c)+";\n"
            procesar_instrucciones_metodo(caso.instrucciones,"switch",ts)
            codigo3d += "goto "+str(br)+";\n"
        else:
            codigo3d += str(c) +":\n"
            print("procesando caso",caso.expNumerica)
            val = resolver_expresion_aritmetica(caso.expNumerica,ts)
            c = getEtiquetaCaso()
            codigo3d += "if("+str(tmp) +" != "+str(val)+") goto "+str(c)+";\n"
            procesar_instrucciones_metodo(caso.instrucciones,"switch",ts)
            codigo3d += "goto "+str(br)+";\n"
        cont += 1
    
    codigo3d += str(c)+":\n"

def procesar_aumento(instr,ts):
    global codigo3d
    print("procesando aumento")
    val = resolver_expresion_aritmetica(instr.expNumerica,ts)
    #tmp = getTemp()
    codigo3d += str(val) + "=" + str(val) + " + 1;\n"
def procesar_decremento(instr,ts):
    global codigo3d
    print("procesando decremento")
    val = resolver_expresion_aritmetica(instr.expNumerica,ts)
    #tmp = getTemp()
    codigo3d += str(val) + "=" + str(val) + " - 1;\n"

def procesar_while(instr,ts):
    print("procesando while")
    global codigo3d
    print("procesando while exp1:",instr.expNumerica," lista:", instr.instrucciones)
    val = resolver_expresion_aritmetica(instr.expNumerica,ts)
    tmp = getTemp()
    w = getWhile()
    lbls = getSalida()
    codigo3d += tmp + "=" + str(val) + ";\n"
    codigo3d += str(w)+":\n"
    codigo3d +="if(" + str(tmp) + ")" + "goto "+str(lbls) +";\n"
    procesar_instrucciones_metodo(instr.instrucciones,w,ts)
    codigo3d += "goto "+str(w)+";\n"
    #codigo3d +=str(lblf)+":\n"
    return lbls

def procesar_dowhile(instr,ts):
    print("procesando do while")
    global codigo3d
    dw = getDoWhile()
    print("procesando do :", instr.instrucciones,"while exp1:",instr.expNumerica)
    #tmp = getTemp()
    w = getWhile()
    lbls = getSalida()
    
    codigo3d += str(dw)+":\n"
    val = resolver_expresion_aritmetica(instr.expNumerica,ts)
    procesar_instrucciones_metodo(instr.instrucciones,dw,ts)
    codigo3d += "goto "+str(w)+";\n"
    codigo3d +=str(w)+":\n"
    codigo3d +="if(" + str(val) + ")" + "goto "+str(dw) +";\n"
    
    codigo3d += "goto "+str(lbls)+";\n"
    #codigo3d +=str(lblf)+":\n"
    return lbls

def procesar_for(instr,ts):
    global codigo3d
    print("procesando for")
    print("asignacion:",instr.asignacion)
    print("expNumerica:",instr.expNumerica)
    print("instr:",instr.instr)
    print("instrucciones:",instr.instrucciones)
    val1 = procesar_asignacion(instr.asignacion,ts)
    
    #codigo3d += str(val1)+ "= "+str(val)+";\n"
    f = getFor()
    lbl = getEtiquetaVerdadera()
    lbls = getSalida()
    codigo3d += str(f)+":\n"
    val = resolver_expresion_aritmetica(instr.expNumerica,ts)
    codigo3d +="if(" + str(val) + ")" + "goto "+str(lbl) +";\n"
    codigo3d += "goto "+str(lbls)+";\n"
    codigo3d +=str(lbl)+":\n"
    if isinstance(instr.instr, Aumento):

        procesar_aumento(instr.instr,ts)
    if isinstance(instr.instr , Decremento):
        procesar_decremento(instr.instr,ts)

    procesar_instrucciones_metodo(instr.instrucciones,f,ts)
    codigo3d += "goto "+str(f)+";\n"
    return lbls
def procesar_metodo(instr, ts):
    global codigo3d
    print("procesando metodo adfasdfasd",instr.id)
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.CADENA, 0,0,instr.id,TS.TIPO_DATO.METODO,0)      # inicializamos con 0 como valor por defecto
    ts.agregar(simbolo)
    codigo3d +=str(instr.id) +":\n"
    procesar_instrucciones_metodo(instr.instrucciones,instr.id,ts)

def procesar_metodo_parametro(instr, ts):
    global codigo3d
    arreglo=[]
    print("procesando metodo parametro",instr.id)
    for p in instr.parametros:
        print(p)
        param = getParam()
        simbolo = TS.Simbolo(p.id, p.tipo, 0,0,instr.id,TS.TIPO_DATO.METODO,param)      # inicializamos con 0 como valor por defecto
        ts.agregar(simbolo)    
        arreglo.append(param)

    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.CADENA, arreglo,0,instr.id,TS.TIPO_DATO.METODO,0)      # inicializamos con 0 como valor por defecto
    ts.agregar(simbolo)
    print(len(instr.parametros))
    codigo3d +=str(instr.id) +":\n"
    procesar_instrucciones_metodo(instr.instrucciones,instr.id,ts)
    
    
    
    

def procesar_struct(instr, ts):
    global codigo3d
    print("procesando struct ",instr)
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.CADENA, 0,0,instr.id,TS.TIPO_DATO.STRUCT,0)      # inicializamos con 0 como valor por defecto
    ts.agregar(simbolo)
    codigo3d +=str(instr.id) +":\n"
    procesar_instrucciones_metodo(instr.instrucciones,instr.id,ts)


    #ts_local = TS.TablaDeSimbolos(ts.simbolos)
    #procesar_instrucciones(instr.instrucciones, ts_local)
    
def getTemp():
    global cont_t
    temp = "$t"+str(cont_t)
    print("temp:",temp)
    cont_t +=1
    return temp
def getParam():
    global cont_p
    temp = "$a"+str(cont_p)
    print("parametro:",temp)
    cont_p +=1
    return temp

def getRetorno():
    global cont_re
    temp = "$v"+str(cont_re)
    print("valor retorno:",temp)
    cont_re +=1
    return temp
def getPika():
    global cont_pila
    temp = "$s"+str(cont_pila)
    print("pila:",temp)
    cont_pila +=1
    return temp
def getEtiquetaVerdadera():
    global cont_e
    lbl = "verdadero"+ str(cont_e)
    print("etiqueta:",lbl)
    cont_e += 1
    return lbl

def getEtiquetaFalsa():
    global cont_ef
    lbl = "falso"+ str(cont_ef)
    print("etiqueta:",lbl)
    cont_ef += 1
    return lbl

def getEtiquetaSwitch():
    global cont_s
    lbl = "switch"+ str(cont_s)
    print("etiqueta:",lbl)
    cont_s += 1
    return lbl

def getEtiquetaCaso():
    global cont_c
    lbl = "caso"+ str(cont_c)
    print("etiqueta:",lbl)
    cont_c += 1
    return lbl

def getBreak():
    global cont_b
    lbl = "break"+ str(cont_b)
    print("etiqueta:",lbl)
    cont_b += 1
    return lbl

def getSalida():
    global cont_salida
    lbl = "salida"+ str(cont_salida)
    print("etiqueta:",lbl)
    cont_salida += 1
    return lbl
def getWhile():
    global cont_w
    lbl = "while"+ str(cont_w)
    print("etiqueta:",lbl)
    cont_w += 1
    return lbl

def getDoWhile():
    global cont_dw
    lbl = "do"+ str(cont_dw)
    print("etiqueta:",lbl)
    cont_dw += 1
    return lbl
def getFor():
    global cont_f
    lbl = "for"+ str(cont_f)
    print("etiqueta:",lbl)
    cont_f += 1
    return lbl
def resolver_expresion_aritmetica(expNum, ts) :
    #print("esta es la expresion ",expNum)
    errores = g.getErrores()
    global codigo3d
    if isinstance(expNum, ExpresionBinaria) :
        print("resolver expresion binaria: ")
        exp1 = resolver_expresion_aritmetica(expNum.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2, ts)
        #print("tipo exp1 :",expNum.exp1.tipo)
        #print("tipo exp2 :",expNum.exp2.tipo)
        if expNum.operador == OPERACION_ARITMETICA.MAS:
            
            expNum.tipo = expNum.exp1.tipo
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"+"+str(exp2)+";\n"
            #print(codigo3d)
            return tmp3
        elif expNum.operador == OPERACION_ARITMETICA.MENOS:
            
            expNum.tipo = expNum.exp1.tipo
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"-"+str(exp2)+";\n"
            #print(codigo3d)
            return tmp3
        elif expNum.operador == OPERACION_ARITMETICA.POR:
           
            expNum.tipo = expNum.exp1.tipo
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"*"+str(exp2)+";\n"
            #print(codigo3d)
            return tmp3
        elif expNum.operador == OPERACION_ARITMETICA.DIVIDIDO:
            
            expNum.tipo = expNum.exp1.tipo
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"/"+str(exp2)+";\n"
            #print(codigo3d)
            return tmp3
        
        elif  expNum.operador == OPERACION_ARITMETICA.RESIDUO:
            
            expNum.tipo = expNum.exp1.tipo
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"%"+str(exp2)+";\n"
            #print(codigo3d)
            return tmp3
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
        elif expNum.operador == OPERACION_RELACIONAL.IGUAL:
            
            expNum.tipo = TS.TIPO_DATO.NUMERO
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"=="+str(exp2)+";\n"
            #print(codigo3d)
            return tmp3
        elif expNum.operador == OPERACION_RELACIONAL.DIFERENTE:
            
            expNum.tipo = TS.TIPO_DATO.NUMERO
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"!="+str(exp2)+";\n"
            #print(codigo3d)
            return tmp3
        elif expNum.operador == OPERACION_RELACIONAL.MAYORIGUAL:
            expNum.tipo = TS.TIPO_DATO.NUMERO
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+">="+str(exp2)+";\n"
            #print(codigo3d)
            return tmp3
        elif expNum.operador == OPERACION_RELACIONAL.MENORIGUAL:
            expNum.tipo = TS.TIPO_DATO.NUMERO
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"<="+str(exp2)+";\n"
            #print(codigo3d)
            return tmp3
        elif expNum.operador == OPERACION_RELACIONAL.MAYOR_QUE:
            
            expNum.tipo = TS.TIPO_DATO.NUMERO
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+">"+str(exp2)+";\n"
            #print(codigo3d)
            return tmp3
        elif expNum.operador == OPERACION_RELACIONAL.MENOR_QUE:
            expNum.tipo = TS.TIPO_DATO.NUMERO
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"<"+str(exp2)+";\n"
            #print(codigo3d)
            return tmp3
        # expresiones logicas
        elif expNum.operador == OPERACION_LOGICA.AND:
            
            expNum.tipo = TS.TIPO_DATO.NUMERO
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"&&"+str(exp2)+";\n"
            #print(codigo3d)
            return tmp3
        elif expNum.operador == OPERACION_LOGICA.OR:
            expNum.tipo = TS.TIPO_DATO.NUMERO
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"||"+str(exp2)+";\n"
            #print(codigo3d)
            return tmp3
        # XOR
        elif expNum.operador == OPERACION_LOGICA.XOR:
            expNum.tipo = TS.TIPO_DATO.NUMERO
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"xor"+str(exp2)+";\n"
            #print(codigo3d)
            return tmp3
        # LOGICAS BITS
        elif expNum.operador == OPERACION_LOGICA.ANDBIT:
            expNum.tipo = TS.TIPO_DATO.NUMERO
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"&"+str(exp2)+";\n"
            #print(codigo3d)
            
            return tmp3
        elif expNum.operador == OPERACION_LOGICA.ORBIT:
            expNum.tipo = TS.TIPO_DATO.NUMERO
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"|"+str(exp2)+";\n"
            #print(codigo3d)
            
            return tmp3
        elif expNum.operador == OPERACION_LOGICA.XORBIT:
            expNum.tipo = TS.TIPO_DATO.NUMERO
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"^"+str(exp2)+";\n"
            #print(codigo3d)
            
            return tmp3
        elif expNum.operador == OPERACION_LOGICA.MENORBIT:
            expNum.tipo = TS.TIPO_DATO.NUMERO
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+"<<"+str(exp2)+";\n"
            #print(codigo3d)
            
            return tmp3
        elif expNum.operador == OPERACION_LOGICA.MAYORBIT:
            expNum.tipo = TS.TIPO_DATO.NUMERO
            tmp3 = getTemp()
            codigo3d += str(tmp3) + "="+str(exp1)+">>"+str(exp2)+";\n"
            #print(codigo3d)
            expNum.val = tmp3
            return tmp3
    elif isinstance(expNum, ExpresionNegativo) :
        tmp = resolver_expresion_aritmetica(expNum.val,ts)
        expNum.tipo = TS.TIPO_DATO.NUMERO
        tmp2 = getTemp()
        codigo3d += str(tmp2) + "=-"+str(tmp)+";\n"
        
        return tmp2
    elif isinstance(expNum, ExpresionEntero) :
        print("expresion enteroasdf:", expNum.tipo)
        if expNum.tipo == TS.TIPO_DATO.CADENA:
            expNum.val = "\""+str(expNum.val)+"\""
            expNum.tipo = expNum.tipo
        elif expNum.tipo == TS.TIPO_DATO.CARACTER:
            
            expNum.val = "\'"+str(expNum.val)+"\'"
            expNum.tipo = expNum.tipo
        elif expNum.tipo == TS.TIPO_DATO.NUMERO:
            expNum.val = str(expNum.val)
            expNum.tipo = expNum.tipo
        elif expNum.tipo == TS.TIPO_DATO.FLOAT:
            expNum.val = str(expNum.val)
            expNum.tipo = expNum.tipo
        
        return expNum.val
    elif isinstance(expNum, ExpresionIdentificador) :
        #print("resolver expresion temporal: ",ts.obtener(expNum.id).valor)
        expNum.val = ts.obtener(expNum.id).temporal
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
        if ts.existeId(expNum.id.id):
            expNum.val = "(int) "+str(ts.obtener(expNum.id.id).temporal)
            expNum.tipo = TS.TIPO_DATO.NUMERO
        return expNum.val
    elif isinstance(expNum, ExpresionConversionFloat):
        #print("resolver expresion conversion float: ", ts.obtener(expNum.id.id).valor)
        if ts.existeId(expNum.id.id):
            expNum.val = "(float) "+str(ts.obtener(expNum.id.id).temporal)
        expNum.tipo = TS.TIPO_DATO.FLOAT
        return expNum.val
    elif isinstance(expNum, ExpresionConversionChar):
        if ts.existeId(expNum.id.id):
            expNum.val = "(char) "+str(ts.obtener(expNum.id.id).temporal)
        expNum.tipo = TS.TIPO_DATO.CHAR
        
        return expNum.val 
    elif isinstance(expNum, ExpresionNot):
        #print("resolver expresion not: ", ts.obtener(expNum.id.id).valor)
        print("es not",expNum.id)
        tmp = resolver_expresion_aritmetica(expNum.id,ts)
        expNum.tipo = TS.TIPO_DATO.NUMERO
        
        tmp2 = getTemp()
        codigo3d += str(tmp2) + "=!"+str(tmp)+";\n"
        
        return tmp2
        
    elif isinstance(expNum, ExpresionNotBit):
        #print("resolver expresion not bit: ", ts.obtener(expNum.id.id).valor)
        tmp = resolver_expresion_aritmetica(expNum.id,ts)
        expNum.tipo = TS.TIPO_DATO.NUMERO
        
        tmp2 = getTemp()
        expNum.val = tmp2
        codigo3d += str(tmp2) + "=~"+str(tmp)+";\n"
        return tmp2
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
            
            procesar_asignacion_arreglo_mul(instrucciones[contador+1],"main", ts)    
        elif isinstance(instrucciones[contador+1], If) :
            
            
            if procesar_if(instrucciones[contador+1], ts) == 1:
                
                return
        
        else : print('Error: instruccion no valida en main')
    
    else:
        print("metodo principal no esta al inicio o no existe")

def procesar_instrucciones_main( instrucciones, ts):
    #print("procesar main")    
    global codigo3d,etiquetas,cont_global
    bandera = False
    param=[]
    print(len(instrucciones))
    for i in instrucciones:
        print("buscamos el main",i.id)
        if i.id == "main":
            bandera = True
            instrucciones = i.instrucciones 
            print(instrucciones)   
            codigo3d +="main:\n"
            for instr in instrucciones :
                
                #print("instruccion:", instr)            
                if isinstance(instr, Imprimir) : 
                    #print("imprimir")
                    procesar_imprimir(instr,ts)
                elif isinstance(instr, ImprimirCompuesto):
                    print("imprimir compuesto")
                    procesar_imprimir_compuesto(instr,ts)
                    #hijo = graficar_imprimir(instr,n_print,ts)
                elif isinstance(instr, Definicion) : 
                    print("definicion",instr.tipo, " ",instr.id[0].id)
                    procesar_definicion(instr,"main",ts)
                    
                elif isinstance(instr, Asignacion):
                    #print("asignacion",instr.id, instr.expNumerica.val)
                    procesar_asignacion(instr,ts)
                    
                elif isinstance(instr, Definicion_Asignacion) : 
                    print("definicion asignacion")
                    procesar_definicion_asignacion(instr,"main", ts)
                    
                    #graficar_asignacion(instr,n_asing,ts)    
                elif isinstance(instr, Definicion_Asignacion_Arreglo) : 
                    print("imprimir")
                    #procesar_asignacion_arreglo(instr, ts) 
                    
                elif isinstance(instr, Definicion_Asignacion_Arreglo_Multiple) : 
                    print("definicion asignacion arreglo mul")
                    procesar_asignacion_arreglo_mul(instr,"main", ts) 
                
                elif isinstance(instr, Etiqueta):
                    print("etiqueta",instr.id)
                    codigo3d += str(instr.id)+":\n"
                elif isinstance(instr, Goto):
                    print("goto",instr.metodo)
                    codigo3d +="goto "+str(instr.metodo)+";\n"
                elif isinstance(instr, Llamada_Funcion):
                    print("llamada funcion",instr.id)
                    l = procesar_llamada_funcion(instr,"main",ts)
                    if l != None:
                        print("no es none llamada")
                        codigo3d += str(l)   +":\n"
                elif isinstance(instr, If) :
                    print("if")
                    
                    s = procesar_if(instr, ts)
                    print("regreso del if",s)
                    if s != None:
                        print("no es none")
                        codigo3d += str(s)+":\n"
                        #return
                elif isinstance(instr, IfElse) :
                    print("ifelse")
                    
                    s = procesar_if_else(instr, ts)
                    print("regreso del if else",s)
                    if s != None:
                        print("no es none el else")
                        codigo3d += str(s)+":\n"
                        #return
                elif isinstance(instr, IfElseIf) :
                    print("es if else if")
                    s = procesar_if_else_if(instr, ts)
                    print("regreso del if else if",s)
                    if s != None:
                        print("no es none el else")
                        codigo3d += str(s)+":\n"
                        #return
                elif isinstance(instr, Switch) :
                    print("switch")
                    
                    sw = procesar_switch(instr, ts)
                    if sw != None:
                        print("no es none switch")
                        codigo3d += str(sw)   +":\n"
                    
                elif isinstance(instr, Definicion_Metodo) : 
                    print("metodo")
                    
                    procesar_metodo(instr,ts)
                    
                elif isinstance(instr, Definicion_Metodo_Parametro) : 
                    print("metodo parametro")
                    
                    procesar_metodo_parametro(instr,ts)
                elif isinstance(instr,Definicion_Struct):
                    print("struct")
                    procesar_struct(instr,ts)
                elif isinstance(instr, Return):
                    print("return")
                
                elif isinstance(instr,Aumento):
                    print("aumento")    
                    procesar_aumento(instr,ts)
                elif isinstance(instr,Decremento):
                    print("decremento")    
                    procesar_decremento(instr,ts)
                elif isinstance(instr, While):
                    print("while")
                    w = procesar_while(instr,ts)
                    if w != None:
                        print("no es none while")
                        codigo3d += str(w)   +":\n"
                elif isinstance(instr, DoWhile):
                    print("do while")
                    d = procesar_dowhile(instr,ts)        
                    if d != None:
                        print("no es none while")
                        codigo3d += str(d)   +":\n"
                elif isinstance(instr, For)       :
                    print("for")
                    f = procesar_for(instr,ts)
                    if f != None:
                        print("no es none for")
                        codigo3d += str(f)+":\n"
                else : print('Error: instruccion no valida en main')
        else:
            
           
            
            
                print("instruccion:", i)            
                if isinstance(i, Imprimir) : 
                    #print("imprimir")
                    procesar_imprimir(i,ts)
                
                    #hijo = graficar_imprimir(instr,n_print,ts)
                elif isinstance(i, ImprimirCompuesto):
                    print("imprimir compuesto")
                    procesar_imprimir_compuesto(i,ts)    
                elif isinstance(i, Definicion) : 
                    print("definicion",i.tipo, " ",i.id)
                    procesar_definicion(i,i.id,ts)
                    
                elif isinstance(i, Asignacion):
                    #print("asignacion",instr.id, instr.expNumerica.val)
                    procesar_asignacion(i,ts)
                    
                elif isinstance(i, Definicion_Asignacion) : 
                    print("definicion asignacion")
                    procesar_definicion_asignacion(i,i.id, ts)
                    
                    #graficar_asignacion(instr,n_asing,ts)    
                elif isinstance(i, Definicion_Asignacion_Arreglo) : 
                    print("definicion asignacion arre")
                    #procesar_asignacion_arreglo(instr, ts) 
                    
                elif isinstance(i, Definicion_Asignacion_Arreglo_Multiple) : 
                    print("definicion asigna arreglo multiple")
                    procesar_asignacion_arreglo_mul(i,i.id, ts) 
                    
                elif isinstance(i, If) :
                    print("if")
                    
                    s = procesar_if(i, ts)
                    print("regreso del if",s)
                    if s != None:
                        print("no es none")
                        codigo3d += str(s)+":\n"
                        #return
                elif isinstance(i, IfElse) :
                    print("ifelse")
                    
                    s = procesar_if_else(i, ts)
                    print("regreso del if else",s)
                    if s != None:
                        print("no es none el else")
                        codigo3d += str(s)+":\n"
                        #return    
                elif isinstance(i, Switch) :
                    print("switch")
                    
                    sw = procesar_switch(i, ts)
                    if sw != None:
                        print("no es none switch")
                        codigo3d += str(sw)   +":\n"
                    
                elif isinstance(i, Definicion_Metodo) : 
                    print("metodo")
                    
                    procesar_metodo(i,ts)
                elif isinstance(i, Definicion_Metodo_Parametro) : 
                    print("metodo parametro")
                    
                    procesar_metodo_parametro(i,ts)
                elif isinstance(i,Definicion_Struct):
                    print("struct")
                    procesar_struct(i,ts)
                elif isinstance(instr, Return):
                    print("return")
                
                elif isinstance(i,Aumento):
                    print("aumento")    
                    procesar_aumento(i,ts)
                elif isinstance(i,Decremento):
                    print("decremento")    
                    procesar_decremento(i,ts)
                elif isinstance(i, While):
                    print("while")
                    w = procesar_while(i,ts)
                    if w != None:
                        print("no es none while")
                        codigo3d += str(w)   +":\n"
                elif isinstance(i, DoWhile):
                    print("do while")
                    d = procesar_dowhile(i,ts)        
                    if d != None:
                        print("no es none while")
                        codigo3d += str(d)   +":\n"
                elif isinstance(i, For)       :
                    print("for")
                    f = procesar_for(i,ts)
                    if f != None:
                        print("no es none for")
                        codigo3d += str(f)+":\n"
                else : print('Error: instruccion no valida en main')
    aux = codigo3d.split("main:",1)
    print(aux)
    print(aux[1:][0])
    print(aux[:-1][0])
    salida = "main:\n"
    
    salida += aux[1:][0]
    salida += aux[:-1][0]
    codigo3d = salida
    print(codigo3d)

             
def procesar_instrucciones_metodo(instrucciones,ambito, ts) :
    ## lista de instrucciones recolectadas
    global codigo3d
    print("procesar metodo",instrucciones)
    
    
    
    #n_metodo=Node("metodo",parent=padre)
    
    for instr in instrucciones :
        print("esto trae el metodo",instr)
            
        if isinstance(instr, Imprimir) : 
                #print("imprimir")
            procesar_imprimir(instr,ts)
               
                #hijo = graficar_imprimir(instr,n_print,ts)
        elif isinstance(instr, ImprimirCompuesto):
            print("imprimir compuesto")
            procesar_imprimir_compuesto(instr,ts)
        elif isinstance(instr, Definicion): 
            print("definicion",instr.tipo, " ",instr.id[0].id)
            procesar_definicion(instr,ambito,ts)
            
        elif isinstance(instr, Asignacion):
            #print("asignacion",instr.id, instr.expNumerica.val)
            procesar_asignacion(instr,ts)
            
        elif isinstance(instr, Definicion_Asignacion) : 
            print("definicion asignacion")
            procesar_definicion_asignacion(instr,ambito, ts)
            
            #graficar_asignacion(instr,n_asing,ts)    
        elif isinstance(instr, Definicion_Asignacion_Arreglo) : 
            print("imprimir")
            #procesar_asignacion_arreglo(instr, ts) 
            
        elif isinstance(instr, Definicion_Asignacion_Arreglo_Multiple) : 
            print("imprimir")
            procesar_asignacion_arreglo_mul(instr,ambito, ts) 
        elif isinstance(instr, Etiqueta):
            print("etiqueta",instr.id)
            codigo3d += str(instr.id)+":\n"
        elif isinstance(instr, Goto):
            print("goto",instr.metodo)
            codigo3d +="goto "+str(instr.metodo)+";\n"    
        elif isinstance(instr, If) :
            print("if")
            
            s = procesar_if(instr, ts)
            print("regreso del if",s)
            if s != None:
                print("no es none")
                codigo3d += str(s)+":\n"
                #return
        elif isinstance(instr, IfElse) :
            print("ifelse")
            
            s = procesar_if_else(instr, ts)
            print("regreso del if else",s)
            if s != None:
                print("no es none el else")
                codigo3d += str(s)+":\n"
                #return    
        elif isinstance(instr, Switch) :
            print("switch")
            
            sw = procesar_switch(instr, ts)
            if sw != None:
                print("no es none switch")
                codigo3d += str(sw)   +":\n"
                
        elif isinstance(instr, Definicion_Metodo) : 
            print("metodo")
            procesar_metodo(instr,ts)
        elif isinstance(instr, Definicion_Struct):
            print("struct")
            procesar_struct(instr,ts)
        elif isinstance(instr, Return):
            print("return")
            
        elif isinstance(instr,Aumento):
            print("aumento")    
            procesar_aumento(instr,ts)
        elif isinstance(instr,Decremento):
            print("decremento")    
            procesar_decremento(instr,ts)
        elif isinstance(instr, While):
            print("while")
            w = procesar_while(instr,ts)
            if w != None:
                print("no es none while")
                codigo3d += str(w)   +":\n"
        elif isinstance(instr, DoWhile):
            print("do while")
            d = procesar_dowhile(instr,ts)        
            if d != None:
                print("no es none while")
                codigo3d += str(d)   +":\n"
        elif isinstance(instr, For)       :
            print("for")
            f = procesar_for(instr,ts)
            if f != None:
                print("no es none for")
                codigo3d += str(f)+":\n"         
        else : print('Error: instruccion no valida metodo')

def procesar_instrucciones_caso(instrucciones, ts) :
    ## lista de instrucciones recolectadas
    global codigo3d
    print("procesar caso")
    #n_metodo=Node("metodo",parent=padre)
    for instr in instrucciones :
        print("esto trae",instr)
            
        if isinstance(instr, Imprimir) : 
                #print("imprimir")
            procesar_imprimir(instr,ts)
               
                #hijo = graficar_imprimir(instr,n_print,ts)
        elif isinstance(instr, ImprimirCompuesto):
            print("imprimir compuesto")
            procesar_imprimir_compuesto(instr,ts)
        elif isinstance(instr, Definicion): 
            print("definicion",instr.tipo, " ",instr.id[0].id)
            procesar_definicion(instr,"caso",ts)
            
        elif isinstance(instr, Asignacion):
            #print("asignacion",instr.id, instr.expNumerica.val)
            procesar_asignacion(instr,ts)
            
        elif isinstance(instr, Definicion_Asignacion) : 
            print("definicion asignacion")
            procesar_definicion_asignacion(instr,"caso", ts)
            
            #graficar_asignacion(instr,n_asing,ts)    
        elif isinstance(instr, Definicion_Asignacion_Arreglo) : 
            print("imprimir")
            #procesar_asignacion_arreglo(instr, ts) 
            
        elif isinstance(instr, Definicion_Asignacion_Arreglo_Multiple) : 
            print("imprimir")
            procesar_asignacion_arreglo_mul(instr,"caso", ts) 
        elif isinstance(instr, Etiqueta):
            print("etiqueta",instr.id)
            codigo3d += str(instr.id)+":\n"
        elif isinstance(instr, Goto):
            print("goto",instr.metodo)
            codigo3d +="goto "+str(instr.metodo)+";\n"    
        elif isinstance(instr, If) :
            print("if")
            
            s = procesar_if(instr, ts)
            print("regreso del if",s)
            if s != None:
                print("no es none")
                codigo3d += str(s)+":\n"
                #return
        elif isinstance(instr, IfElse) :
            print("ifelse")
            
            s = procesar_if_else(instr, ts)
            print("regreso del if else",s)
            if s != None:
                print("no es none el else")
                codigo3d += str(s)+":\n"
                #return    
        elif isinstance(instr, Switch) :
            print("switch")
            
            sw = procesar_switch(instr, ts)
            if sw != None:
                print("no es none switch")
                codigo3d += str(sw)   +":\n"
                
        elif isinstance(instr, Definicion_Metodo) : 
            print("metodo")
            procesar_metodo(instr,ts)
        elif isinstance(instr, Definicion_Struct):
            print("struct")
            procesar_struct(instr,ts)
        elif isinstance(instr, Return):
            print("return")
            
        elif isinstance(instr,Aumento):
            print("aumento")    
            procesar_aumento(instr,ts)
        elif isinstance(instr,Decremento):
            print("decremento")    
            procesar_decremento(instr,ts)
        elif isinstance(instr, While):
            print("while")
            w = procesar_while(instr,ts)
            if w != None:
                print("no es none while")
                codigo3d += str(w)   +":\n"
        elif isinstance(instr, DoWhile):
            print("do while")
            d = procesar_dowhile(instr,ts)        
            if d != None:
                print("no es none while")
                codigo3d += str(d)   +":\n"
        elif isinstance(instr, For)       :
            print("for")
            f = procesar_for(instr,ts)
            if f != None:
                print("no es none for")
                codigo3d += str(f)+":\n"         
        else : print('Error: instruccion no valida caso')


def graficar_arbol(instrucciones):
    raiz = Node("root")
    metodo = raiz
    contador = 0
    instr_restantes = []
    for instr in instrucciones :   
        if isinstance(instr, Imprimir) : 
            n_print= Node("imprimir", parent=raiz)
            #hijo = Node(instr.cad,parent=n_print)
        elif isinstance(instr, ImprimirCompuesto):
            n_printc= Node("imprimirC", parent=raiz)
        elif isinstance(instr,Definicion):
            n_def = Node("definicion",parent=raiz)
        elif isinstance(instr, Asignacion):
            n_asing = Node("asignacion", parent=raiz)
        elif isinstance(instr, Definicion_Asignacion) : 
            n_asing= Node("def_asignar", parent=raiz)
            #graficar_hijos(instr,n_asing)
        elif isinstance(instr, Definicion_Asignacion_Arreglo) : 
            n_arr = Node("asignar arreglo", parent=raiz)
            
        elif isinstance(instr, Definicion_Asignacion_Arreglo_Multiple) : 
            n_arr_m = Node("asignar arreglo multiple",parent=raiz)    
        elif isinstance(instr, If) : 
            n_if = Node("if",parent=raiz)
            graficar_hijos(instr.instrucciones,n_if)
        elif isinstance(instr, IfElse) : 
            n_ifelse = Node("ifelse",parent=raiz)   
            graficar_hijos(instr.instrIfVerdadero,n_ifelse)
            graficar_hijos(instr.instrIfFalso,n_ifelse)                       
        elif isinstance(instr, IfElseIf) : 
            n_ifelseif = Node("ifelseif",parent=raiz)
            graficar_hijos(instr.instrIfVerdadero,n_ifelseif)
            graficar_hijos(instr.expNumerica2,n_ifelseif) 
        elif isinstance(instr, Definicion_Metodo) :             
            n_metodo = Node("metodo",parent=raiz)
            graficar_hijos(instr.instrucciones,n_metodo)
                   
        elif isinstance(instr, Definicion_Metodo_Parametro) :             
            n_metodoP = Node("metodoP",parent=raiz)
            graficar_hijos(instr.instrucciones,n_metodoP)
        elif isinstance(instr, Etiqueta):
            n_etiqueta = Node("etiqueta",parent=raiz)            
        elif isinstance(instr, Goto) : 
            #print("entro al goto")
            n_goto = Node("goto",parent=raiz)
        elif isinstance(instr, While):
            n_while = Node("while",parent=raiz)
            graficar_hijos(instr.instrucciones,n_while)
        elif isinstance(instr, Llamada_Funcion):
            n_llamada = Node("llamada",parent=raiz)
        elif isinstance(instr, Switch) :
            n_switch = Node("switch",parent=raiz)
        elif isinstance(instr, Aumento) :
            n_aumento = Node("aumento",parent=raiz)
        elif isinstance(instr, Decremento) :
            n_decremento = Node("decremento",parent=raiz)
        elif isinstance(instr, DoWhile) :
            n_dowhile = Node("dowhile",parent=raiz)
        
            
        else : print('Error: instruccion no valida graficar')
        
    UniqueDotExporter(raiz).to_picture("ast2.png") 

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
        elif isinstance(instr, IfElse) : 
            n_if = Node("ifelse",parent=raiz)                        
        elif isinstance(instr, IfElseIf) : 
            n_if = Node("ifelseif",parent=raiz)
        elif isinstance(instr, Definicion_Metodo) : 
            n_metodo = Node("metodo",parent=raiz)
            graficar_hijos(instr.instrucciones,n_metodo)
        elif isinstance(instr, Definicion_Metodo_Parametro): 
            n_metodo = Node("metodoP",parent=raiz)
            graficar_hijos(instr.instrucciones,n_metodo)            
            
        elif isinstance(instr, Etiqueta):
            n_etiqueta = Node("etiqueta",parent=raiz)            
        elif isinstance(instr, Goto) : 
            #print("entro al goto")
            n_goto = Node("goto",parent=raiz)
        elif isinstance(instr, While):
            n_while = Node("while",parent=raiz)
            graficar_hijos(instr.instrucciones,n_while)
        elif isinstance(instr, Llamada_Funcion):
            n_llamada = Node("llamada",parent=raiz)
        elif isinstance(instr, Switch) :
            n_switch = Node("switch",parent=raiz)
        elif isinstance(instr, Aumento) :
            n_aumento = Node("aumento",parent=raiz)
        elif isinstance(instr, Decremento) :
            n_decremento = Node("decremento",parent=raiz)
        elif isinstance(instr, DoWhile) :
            n_dowhile = Node("dowhile",parent=raiz)           
        
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
        #print("esto trae:",gram)
        nodo += '<TR><TD>'+gram+'</TD></TR>'
        
    #print("nodo",nodo)    
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

#f = open("./entrada2.txt", "r")
#input = f.read()

#instrucciones = g.parse(input)
#errores = g.getErrores()
#print("eso trae la lista_errores", errores)           

#print("primer print:",instrucciones)
#ts_global = TS.TablaDeSimbolos()
#graficar_arbol(instrucciones)
#procesar_instrucciones_main(instrucciones, ts_global)
#generar_arbol(instrucciones,ts_global)
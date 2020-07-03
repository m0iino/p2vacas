# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 00:13:39 2020

@author: moino
"""

class Instruccion:
    '''This is an abstract class'''

class Imprimir(Instruccion) :
    '''
        Esta clase representa la instrucción imprimir.
        La instrucción imprimir únicamente tiene como parámetro una cadena
    '''

    def __init__(self,  cad) :
        self.cad = cad
class ImprimirCompuesto(Instruccion):
    def __init__(self,cad,ids):
        self.cad = cad
        self.ids = ids
class Borrar(Instruccion) :
    def __init__(self,  cad) :
        self.cad = cad

class Mientras(Instruccion) :
    '''
        Esta clase representa la instrucción mientras.
        La instrucción mientras recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, expLogica, instrucciones = []) :
        self.expLogica = expLogica
        self.instrucciones = instrucciones
class While(Instruccion):
    def __init__(self,expNumerica,instrucciones):
        self.expNumerica = expNumerica
        self.instrucciones = instrucciones

class DoWhile(Instruccion):
    def __init__(self,instrucciones,expNumerica):
        self.instrucciones = instrucciones
        self.expNumerica = expNumerica
        
class For(Instruccion):
    def __init__(self, asignacion,expNumerica,instr,instrucciones):
        self.asignacion = asignacion
        self.expNumerica = expNumerica
        self.instr = instr
        self.instrucciones = instrucciones
class Aumento(Instruccion):
    def __init__(self,expNumerica):
        self.expNumerica = expNumerica

class Decremento(Instruccion):
    def __init__(self,expNumerica):
        self.expNumerica = expNumerica
        
class Definicion(Instruccion) :
    '''
        Esta clase representa la instrucción de definición de variables.
        Recibe como parámetro el nombre del identificador a definir
    '''

    def __init__(self, tipo, id) :
        self.tipo = tipo
        self.id = id
class DefifnicionLista(Instruccion):
    def __init__(self,tipo,ids = []):
        self.tipo = tipo
        self.ids = ids

class Asignacion(Instruccion) :
    '''
        Esta clase representa la instrucción de asignación de variables
        Recibe como parámetro el identificador a asignar y el valor que será asignado.
    '''

    def __init__(self, id, expNumerica) :
        self.id = id
        self.expNumerica = expNumerica

class Definicion_Asignacion(Instruccion) :
    '''
        Esta clase representa la instrucción de asignación de variables
        Recibe como parámetro el identificador a asignar y el valor que será asignado.
    '''

    def __init__(self, tipo, id , expNumerica) :
        self.tipo = tipo
        self.id = id
        self.expNumerica = expNumerica

class Etiqueta(Instruccion):
    def __init__(self,id):
        self.id = id


        
class Definicion_Asignacion_Arreglo(Instruccion) :
    '''
        Esta clase representa la instrucción de asignación de variables
        Recibe como parámetro el identificador a asignar y el valor que será asignado.
    '''

    def __init__(self, tipo,id, expNumerica , expNumerica2) :
        self.tipo = tipo
        self.id = id
        self.expNumerica = expNumerica
        self.expNumerica2 = expNumerica2

class Definicion_Asignacion_Arreglo_Multiple(Instruccion) :
    '''
        Esta clase representa la instrucción de asignación de variables
        Recibe como parámetro el identificador a asignar y el valor que será asignado.
    '''

    def __init__(self,tipo, id, expNumerica , expNumerica2) :
        self.tipo = tipo
        self.id = id
        self.expNumerica = expNumerica
        self.expNumerica2 = expNumerica2

class Llamada_Funcion(Instruccion):
    def __init__(self,id,ids):
        self.id = id
        self.ids = ids
class Scanf(Instruccion):
    def __init__(self,id):
        self.id = id

class If(Instruccion) : 
    '''
        Esta clase representa la instrucción if.
        La instrucción if recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, expNumerica, instrucciones) :
        self.expNumerica = expNumerica
        self.instrucciones = instrucciones
        
class IfElse(Instruccion):
    def __init__(self,expNumerica,instrIfVerdadero, instrIfFalso):
        self.expNumerica = expNumerica
        self.instrIfVerdadero = instrIfVerdadero
        self.instrIfFalso = instrIfFalso
class IfElseIf(Instruccion):
    def __init__(self,expNumerica,instrIfVerdadero,expNumerica2):
        self.expNumerica = expNumerica
        self.instrIfVerdadero = instrIfVerdadero
        self.expNumerica2 = expNumerica2
class Switch(Instruccion):
    def __init__(self,expNumerica, casos):
        self.expNumerica = expNumerica
        self.casos = casos
class Caso(Instruccion):
    def __init__(self,expNumerica,instrucciones):
        self.expNumerica = expNumerica
        self.instrucciones = instrucciones

class Default(Instruccion):
    def __init__(self,instrucciones):
        self.instrucciones = instrucciones

class Definicion_Struct(Instruccion):
    def __init__(self,id,tipo,instrucciones):
        self.id = id
        self.tipo = tipo
        self.instrucciones = instrucciones

class Definicion_Metodo(Instruccion):
    def __init__(self, id, tipo,instrucciones):
        self.id = id
        self.tipo = tipo
        self.instrucciones = instrucciones
class Definicion_Metodo_Parametro(Instruccion):
    def __init__(self,tipo,id,parametros,instrucciones):
        self.tipo = tipo
        self.id = id
        
        self.parametros = parametros
        self.instrucciones = instrucciones
class Return(Instruccion):
    def __init__(self, expNumerica):
        self.expNumerica = expNumerica
class Break(Instruccion):
    def __init__(self,id):
        self.id = id
    
class Goto(Instruccion):
    def __init__(self,metodo):
        self.metodo= metodo
        
class Exit(Instruccion):
    def __init__(self, expNumerica):
        self.expNumerica = expNumerica
        
class Parametro(Instruccion):
    def __init__(self,tipo,id):
        self.tipo = tipo
        self.id = id
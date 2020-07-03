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

class Definicion(Instruccion) :
    '''
        Esta clase representa la instrucción de definición de variables.
        Recibe como parámetro el nombre del identificador a definir
    '''

    def __init__(self, id) :
        self.id = id

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

    def __init__(self, id, expNumerica) :
        self.id = id
        self.expNumerica = expNumerica


class Definicion_Asignacion_Arreglo(Instruccion) :
    '''
        Esta clase representa la instrucción de asignación de variables
        Recibe como parámetro el identificador a asignar y el valor que será asignado.
    '''

    def __init__(self, id, expNumerica , expNumerica2) :
        self.id = id
        self.expNumerica = expNumerica
        self.expNumerica2 = expNumerica2

class Definicion_Asignacion_Arreglo_Multiple(Instruccion) :
    '''
        Esta clase representa la instrucción de asignación de variables
        Recibe como parámetro el identificador a asignar y el valor que será asignado.
    '''

    def __init__(self, id, expNumerica , expNumerica2) :
        self.id = id
        self.expNumerica = expNumerica
        self.expNumerica2 = expNumerica2


class If(Instruccion) : 
    '''
        Esta clase representa la instrucción if.
        La instrucción if recibe como parámetro una expresión lógica y la lista
        de instrucciones a ejecutar si la expresión lógica es verdadera.
    '''

    def __init__(self, expNumerica, expNumerica2) :
        self.expNumerica = expNumerica
        self.expNumerica2 = expNumerica2


class Definicion_Metodo(Instruccion):
    def __init__(self, id, instrucciones = []):
        self.id = id
        self.instrucciones = instrucciones
        
class Goto(Instruccion):
    def __init__(self,metodo):
        self.metodo= metodo
        
class Exit(Instruccion):
    def __init__(self, expNumerica):
        self.expNumerica = expNumerica
        
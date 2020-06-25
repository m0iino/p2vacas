# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 00:04:07 2020

@author: moino
"""

from enum import Enum

class OPERACION_ARITMETICA(Enum) :
    MAS = 1
    MENOS = 2
    POR = 3
    DIVIDIDO = 4
    RESIDUO = 5
    ABSOLUTO = 6
    
class OPERACION_LOGICA(Enum) :
    MAYOR_QUE = 1
    MENOR_QUE = 2
    IGUAL = 3
    DIFERENTE = 4
    NOT = 5
    AND = 6
    OR = 7
    XOR = 8
    NOTBIT=9
    ANDBIT = 10
    ORBIT = 11
    XORBIT =12
    MENORBIT = 13
    MAYORBIT = 14
class OPERACION_RELACIONAL(Enum):
    MAYOR_QUE = 1
    MENOR_QUE = 2
    IGUAL = 3
    DIFERENTE = 4
    MAYORIGUAL = 5
    MENORIGUAL = 6
    
class ExpresionNumerica:
    '''
        Esta clase representa una expresión numérica
    '''
class ExpresionEntero:
    def __init__(self, val = 0, tipo = 0, linea=0):
        self.val = val
        self.tipo = tipo
        self.linea = linea

class ExpresionArreglo:
    def __init__(self, id,val = 0, tipo = 0):
        self.id = id
        self.val = val
        self.tipo = tipo
        
class AccesoArreglo(ExpresionNumerica):
    def __init__(self, id, expNumerica ) :
        self.id = id
        self.expNumerica = expNumerica
    

class ExpresionBinaria(ExpresionNumerica) :
    '''
        Esta clase representa la Expresión Aritmética Binaria.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador
        
class ExpresionAbsoluto(ExpresionNumerica):
    def __init__(self,id = ""):
        self.id = id

class ExpresionConversionInt(ExpresionNumerica):
    def __init__(self,id = ""):
        self.id = id
class ExpresionConversionFloat(ExpresionNumerica):
    def __init__(self,id = ""):
        self.id = id
class ExpresionConversionChar(ExpresionNumerica):
    def __init__(self,id = ""):
        self.id = id
class ExpresionNot(ExpresionNumerica):
    def __init__(self,id = ""):
        self.id = id

class ExpresionNotBit(ExpresionNumerica):
    def __init__(self,id = ""):
        self.id = id
class ExpresionNegativo:
    def __init__(self, val =0, tipo = 0):
        self.val = val
        self.tipo = tipo


class ExpresionNumero(ExpresionNumerica) :
    '''
        Esta clase representa una expresión numérica entera o decimal.
    '''

    def __init__(self, val = 0) :
        self.val = val

class ExpresionDecimal(ExpresionNumerica) :
    '''
        Esta clase representa una expresión numérica entera o decimal.
    '''

    def __init__(self, val = 0) :
        self.val = val


class ExpresionIdentificador(ExpresionNumerica) :
    '''
        Esta clase representa un identificador.
    '''

    def __init__(self, id,linea) :
        self.id = id
        self.linea = linea



class ExpresionCadena :
    '''
        Esta clase representa una Expresión de tipo cadena.
    '''
 
class ExpresionCaracter(ExpresionCadena) :
    def __init__(self, val) :
        self.val = val

    
    
class ExpresionConcatenar(ExpresionCadena) :
    '''
        Esta clase representa una Expresión de tipo cadena.
        Recibe como parámetros las 2 expresiones a concatenar
    '''

    def __init__(self, exp1, exp2) :
        self.exp1 = exp1
        self.exp2 = exp2


class ExpresionDobleComilla(ExpresionCadena) :
    '''
        Esta clase representa una cadena entre comillas doble.
        Recibe como parámetro el valor del token procesado por el analizador léxico
    '''

    def __init__(self, val) :
        self.val = val


class ExpresionCadenaNumerico(ExpresionCadena) :
    '''
        Esta clase representa una expresión numérica tratada como cadena.
        Recibe como parámetro la expresión numérica
    '''
    def __init__(self, exp) :
        self.exp = exp
class ExpresionCadenaCaracter(ExpresionCadena) :
    '''
        Esta clase representa una expresión caracter tratada como cadena.
        Recibe como parámetro la expresión numérica
    '''
    def __init__(self, exp) :
        self.exp = exp

class ExpresionLogica() :
    '''
        Esta clase representa la expresión lógica.
        Esta clase recibe los operandos y el operador
    '''

    def __init__(self, exp1, exp2, operador) :
        self.exp1 = exp1
        self.exp2 = exp2
        self.operador = operador


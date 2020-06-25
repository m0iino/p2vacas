# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 00:15:09 2020

@author: moino
"""

from enum import Enum

class TIPO_DATO(Enum) :
    NUMERO = 1
    FLOAT = 2
    CHAR = 3
    CADENA = 4
    CARACTER = 5
    ARREGLO = 6
    STRUCT = 7
    TEMP = 8
    ERROR = 9
    UNARIO = 10
    ABS = 11
    METODO =12
    ID = 13
class Simbolo() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, id, tipo, valor) :
        self.id = id
        self.tipo = tipo
        self.valor = valor

class TablaDeSimbolos() :
    'Esta clase representa la tabla de simbolos'

    def __init__(self, simbolos = {}) :
        self.simbolos = simbolos

    def agregar(self, simbolo) :
        self.simbolos[simbolo.id] = simbolo
        
    def obtener(self, id) :
        if not id in self.simbolos :
            print('Error obtener: variable ', id, ' no definida.')
            

        return self.simbolos[id]

    def actualizar(self, simbolo) :
        if not simbolo.id in self.simbolos :
            print('Error actualizar: variable ', simbolo.id, ' no definida.')
        else :
            self.simbolos[simbolo.id] = simbolo
    def existe(self, simbolo):
        if not simbolo.id in self.simbolos:
            return False
        else :
            return True
    def borrar(self, id):
        if not id in self.simbolos:
            print("Error: variable ", id, " no definido.")
        else:
            print("temporal borrado: ",id)
            self.simbolos.pop(id)
    
        
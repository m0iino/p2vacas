reservadas = {
    'numero' : 'NUMERO',
    'print' : 'IMPRIMIR',
    'mientras' : 'MIENTRAS',
    'abs' : 'ABS',
    'unset' : 'UNSET',
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'if' : 'IF',
    'xor' : 'XOR',
    'array' : 'ARRAY',
    'goto' : 'GOTO',
    'exit' : 'EXIT'
}

tokens  = [
    'PTCOMA',
    'DOSPUNTOS',
    'LLAVIZQ',
    'LLAVDER',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'CONCAT',
    'MENQUE',
    'MAYQUE',
    'IGUALQUE',
    'NIGUALQUE',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID',
    'TEMP',
    'PARAM',
    'VAL',
    'PILA',
    'PUNTERO',
    'DIR',
    'CARACTER',
    'RESIDUO',
    'NOT',
    'NOTBIT',
    'AND',
    'ANDBIT',
    'OR',
    'ORBIT',
    
    'XORBIT',
    'MENORBIT',
    'MAYORBIT',
    'MENIGUAL',
    'MAYIGUAL'
    
] + list(reservadas.values())

# Tokens
t_PTCOMA    = r';'
t_DOSPUNTOS = r':'
t_LLAVIZQ   = r'{'
t_LLAVDER   = r'}'
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_CORIZQ    = r'\['
t_CORDER    = r'\]'
t_IGUAL     = r'='
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_NOT = r'!'
t_NOTBIT = r'\~'
t_CONCAT    = r'&y'
t_AND = r'&&'
t_ANDBIT = r'&'

t_XORBIT = r'\^'
t_MENORBIT = r'<<'
t_MAYORBIT = r'>>'
t_OR = r'\|\|'
t_ORBIT = r'\|'
t_MENIGUAL = r'<='
t_MAYIGUAL = r'>='
t_MENQUE    = r'<'
t_MAYQUE    = r'>'
t_IGUALQUE  = r'=='
t_NIGUALQUE = r'!='
t_RESIDUO = r'%'
import ts as TS

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t
     
def t_TEMP(t):
     r'\$t[0-9]+'
     t.type = reservadas.get(t.value.lower(),'TEMP')    # Check for reserved words
     return t

def t_PARAM(t):
     r'\$a[0-9]+'
     t.type = reservadas.get(t.value.lower(),'PARAM')    # Check for reserved words
     return t   

def t_VAL(t):
     r'\$v[0-9]+'
     t.type = reservadas.get(t.value.lower(),'VAL')    # Check for reserved words
     return t
     
def t_PILA(t):
     r'\$s[0-9]+'
     t.type = reservadas.get(t.value.lower(),'PILA')    # Check for reserved words
     return t
     
def t_PUNTERO(t):
     r'\$sp'
     t.type = reservadas.get(t.value.lower(),'PUNTERO')    # Check for reserved words
     return t

def t_DIR(t):
     r'\$ra'
     t.type = reservadas.get(t.value.lower(),'DIR')    # Check for reserved words
     return t
     

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_CARACTER(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'//.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    #print("Illegal character '%s'" % t.value[0])
    #print("columna",str(find_column(t.lexer.lexdata,t)))
    error = "Error lexico en el lexema: \'"+ t.value[0]+"\' la linea: " + str(t.lexer.lineno) + " columna: " + str(find_column(t.lexer.lexdata,t))
    lista_errores.append(error)
    t.lexer.skip(1)

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()
lista_errores = []

# Asociación de operadores y precedencia
precedence = (
    ('right', 'NOT'),
    ('right','NOTBIT'),
    ('left', 'AND','OR','XOR'),
    ('left', 'XORBIT'),
    ('left', 'ANDBIT','ORBIT'),
    ('left', 'MENORBIT','MAYORBIT'),
    ('left', 'IGUALQUE', 'NIGUALQUE'),
    ('left', 'MENQUE', 'MAYQUE'),
    ('left','CONCAT'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    ('left','RESIDUO'),
    ('right','UMENOS'),
    )

# Definición de la gramática

from expresiones import *
from instrucciones import *
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from anytree.exporter import UniqueDotExporter
gramatical = []
n_init = Node("raiz")
def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]
    global gramatical 
    gramatical.append( " inicio.val : instrucciones.val")
def p_instrucciones_lista(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]
    global gramatical 
    gramatical.append( " instrucciones.val : instrucciones1.append(instruccion.val)")

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]
    global gramatical 
    gramatical.append( " instrucciones.val: instruccion.val")
def p_instruccion(t) :
    '''instruccion      : imprimir_instr                                           
                        | asignacion_temp
                        | asignacion_param
                        | asignacion_val
                        | asignacion_dir
                        | asignacion_pila
                        | asignacion_puntero
                        | borrar_temp
                        | if_instr
                        | metodo
                        | goto
                        | exit'''
    t[0] = t[1]
    global gramatical 
    gramatical.append( " instruccion.val: expresiones.val")

def p_definir_exit(t):
    'exit : EXIT PTCOMA'
    t[0] = Exit(t[1])
    global gramatical 
    gramatical.append( "exit.val : exit.val")
def p_definir_metodo(t):
    'metodo : ID DOSPUNTOS'
    t[0] = Definicion_Metodo(t[1])
    global gramatical 
    gramatical.append( " metodo.val : id.val")

def p_instruccion_imprimir(t) :
    'imprimir_instr     : IMPRIMIR PARIZQ expresion_numerica PARDER PTCOMA'
    t[0] =Imprimir(t[3])
    global gramatical 
    gramatical.append( " imprimir.val : expresion.val")
def p_borrar_temp(t):
    'borrar_temp : UNSET PARIZQ expresion_numerica PARDER PTCOMA'
    t[0] = Borrar(t[3])
    global gramatical 
    gramatical.append( " borrar.val : expresion.val")
def p_asignacion_temporal(t):
    'asignacion_temp   : TEMP IGUAL expresion_numerica PTCOMA'
    
    t[0] = Definicion_Asignacion(t[1], t[3])
    global gramatical 
    gramatical.append( " asignartemp.val : expresion.val")
def p_asignacion_parametro(t):
    'asignacion_param   : PARAM IGUAL expresion_numerica PTCOMA'
    
    t[0] = Definicion_Asignacion(t[1], t[3])
    global gramatical 
    gramatical.append( " asignarpar.val : expresion.val")
def p_asignacion_val(t):
    'asignacion_val   : VAL IGUAL expresion_numerica PTCOMA'
    
    t[0] = Definicion_Asignacion(t[1], t[3])
    global gramatical 
    gramatical.append( " asignarval.val : expresion.val")
def p_asignacion_dir(t):
    'asignacion_dir   : DIR IGUAL expresion_numerica PTCOMA'
    
    t[0] = Definicion_Asignacion(t[1], t[3])
    global gramatical 
    gramatical.append( " asignardir.val : expresion.val")
def p_asignacion_pila(t):
    'asignacion_pila   : PILA IGUAL expresion_numerica PTCOMA'
    
    t[0] = Definicion_Asignacion(t[1], t[3])
    global gramatical 
    gramatical.append( " asignarpila.val : expresion.val")
def p_asignacion_puntero(t):
    'asignacion_puntero   : PUNTERO IGUAL expresion_numerica PTCOMA'
    
    t[0] = Definicion_Asignacion(t[1], t[3])
    global gramatical 
    gramatical.append( " asignarpuntero.val : expresion.val")

def p_asignacion_arreglo_multi(t):
    'asignacion_temp : TEMP dimensiones IGUAL expresion_numerica PTCOMA'
    t[0] = Definicion_Asignacion_Arreglo_Multiple(t[1],t[2],t[4])
    global gramatical 
    gramatical.append("asignararrmu.val : expresion.val ")
def p_asignacion_arreglo_multi_pila(t):
    'asignacion_temp : PILA dimensiones IGUAL expresion_numerica PTCOMA'
    t[0] = Definicion_Asignacion_Arreglo_Multiple(t[1],t[2],t[4])
    global gramatical 
    gramatical.append("asignararrmupila.val : expresion.val")

def p_acceso_arreglo(t):
    'expresion_numerica : TEMP dimensiones'
    t[0] = AccesoArreglo(t[1],t[2])
    global gramatical 
    gramatical.append("expresion.val : dimensiones.val")
def p_acceso_arreglo_par(t):
    'expresion_numerica : PILA dimensiones'
    t[0] = AccesoArreglo(t[1],t[2])
    global gramatical 
    gramatical.append("expresion.val : dimensiones.val")     
def p_dimensiones_lista(t):
    'dimensiones : dimensiones dimension'
    t[1].append(t[2])
    t[0] = t[1]
    global gramatical 
    gramatical.append( " dimensiones.val : dimensiones1.append(dimension.val)")
def p_dimensiones(t)    :
    'dimensiones : dimension'
    t[0] = [t[1]]
    global gramatical 
    gramatical.append( " dimensiones.val : dimension.val")
def p_dimension(t):
    'dimension : CORIZQ expresion_numerica CORDER'
    t[0]= t[2]
    global gramatical 
    gramatical.append( " dimension.val : expresion.val")
def p_if_instr(t) :
    'if_instr  : IF PARIZQ expresion_numerica PARDER expresion_numerica'
    t[0] =If(t[3], t[5])
    global gramatical 
    gramatical.append( " if.val : dimensiones.val")


def p_expresion_binaria(t):
    '''expresion_numerica : expresion_numerica MAS expresion_numerica
                        | expresion_numerica MENOS expresion_numerica
                        | expresion_numerica POR expresion_numerica
                        | expresion_numerica DIVIDIDO expresion_numerica
                        | expresion_numerica RESIDUO expresion_numerica'''
    global gramatical 
    if t[2] == '+'  : 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MAS)
        gramatical.append( " expresion.val : expresion.val + expresion.val")
    elif t[2] == '-': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.MENOS)
        gramatical.append( " expresion.val : expresion.val - expresion.val")
    elif t[2] == '*': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.POR)
        gramatical.append( " expresion.val : expresion.val * expresion.val")
    elif t[2] == '/': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.DIVIDIDO)
        gramatical.append( " expresion.val : expresion.val  expresion.val")
    elif t[2] == '%': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_ARITMETICA.RESIDUO)
        gramatical.append( " expresion.val : expresion.val '\%' expresion.val")
def p_expresion_binaria_realacional(t):
    '''expresion_numerica : expresion_numerica IGUALQUE expresion_numerica
                        | expresion_numerica NIGUALQUE expresion_numerica
                        | expresion_numerica MAYIGUAL expresion_numerica
                        | expresion_numerica MENIGUAL expresion_numerica
                        | expresion_numerica MAYQUE expresion_numerica
                        | expresion_numerica MENQUE expresion_numerica'''
    global gramatical 
    if t[2] == '=='  : 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_RELACIONAL.IGUAL)
        gramatical.append( " expresion.val : expresion.val igualigual expresion.val")
    elif t[2] == '!=': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_RELACIONAL.DIFERENTE)
        gramatical.append( " expresion.val : expresion.val notigual expresion.val")
    elif t[2] == '>=': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_RELACIONAL.MAYORIGUAL)
        gramatical.append( " expresion.val : expresion.val mayorigual expresion.val")
    elif t[2] == '<=': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_RELACIONAL.MENORIGUAL)
        gramatical.append( " expresion.val : expresion.val menorigual expresion.val")
    elif t[2] == '>': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_RELACIONAL.MAYOR_QUE)
        gramatical.append( " expresion.val : expresion.val mayor expresion.val")
    elif t[2] == '<': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_RELACIONAL.MENOR_QUE)
        gramatical.append( " expresion.val : expresion.val menor expresion.val")

def p_expresion_binaria_logica(t):
    '''expresion_numerica : expresion_numerica AND expresion_numerica
                        | expresion_numerica OR expresion_numerica
                        | expresion_numerica XOR expresion_numerica'''
    if t[2] == '&&'  : t[0] = ExpresionBinaria(t[1], t[3], OPERACION_LOGICA.AND)
    elif t[2] == '||': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_LOGICA.OR)
    elif t[2] == 'xor': t[0] = ExpresionBinaria(t[1], t[3], OPERACION_LOGICA.XOR)

def p_expresion_binaria_bit(t):
    '''expresion_numerica : expresion_numerica ANDBIT expresion_numerica
                        | expresion_numerica ORBIT expresion_numerica
                        | expresion_numerica XORBIT expresion_numerica
                        | expresion_numerica MAYORBIT expresion_numerica
                        | expresion_numerica  MENORBIT expresion_numerica'''
    global gramatical 
    if t[2] == '&'  : 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_LOGICA.ANDBIT)
        gramatical.append( " expresion.val : expresion.val & expresion.val")
    elif t[2] == '|': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_LOGICA.ORBIT)
        gramatical.append( " expresion.val : expresion.val | expresion.val")
    elif t[2] == '^': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_LOGICA.XORBIT)
        gramatical.append( " expresion.val : expresion.val ^ expresion.val")
    elif t[2] == '<<': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_LOGICA.MENORBIT)
        gramatical.append( " expresion.val : expresion.val << expresion.val")
    elif t[2] == '>>': 
        t[0] = ExpresionBinaria(t[1], t[3], OPERACION_LOGICA.MAYORBIT)   
             
        gramatical.append( " expresion.val : expresion.val >> expresion.val")
    
def p_expresion_not(t):
    'expresion_numerica : NOT expresion_numerica'
    t[0] = ExpresionNot(t[2])
    global gramatical 
    gramatical.append( " expresion.val : expresion.val")
def p_expresion_notbit(t):
    'expresion_numerica : NOTBIT expresion_numerica'
    t[0] = ExpresionNotBit(t[2])
    global gramatical 
    gramatical.append( " expresion.val : expresion.val")
def p_conversion_int(t):
    'expresion_numerica : PARIZQ INT PARDER expresion_numerica'
    t[0] = ExpresionConversionInt(t[4])
    global gramatical 
    gramatical.append( " expresion.val : expresion.val")
def p_conversion_float(t):
    'expresion_numerica : PARIZQ FLOAT PARDER expresion_numerica'
    t[0] = ExpresionConversionFloat(t[4])
    global gramatical 
    gramatical.append( " expresion.val : expresion.val")
def p_conversion_char(t):
    'expresion_numerica : PARIZQ CHAR PARDER expresion_numerica'
    t[0] = ExpresionConversionChar(t[4])
    global gramatical 
    gramatical.append( " expresion.val : expresion.val")
def p_expresion_unaria(t):
    'expresion_numerica : MENOS expresion_numerica %prec UMENOS'
    t[0] = ExpresionNegativo(t[2], TS.TIPO_DATO.NUMERO)
    global gramatical 
    gramatical.append( " expresion.val : expresion.val")
def p_expresion_absoluto(t):
    'expresion_numerica : ABS PARIZQ expresion_numerica PARDER'
    t[0] = ExpresionAbsoluto(t[3])
    global gramatical 
    gramatical.append( " expresion.val : expresion.val")
def p_expresion_agrupacion(t):
    'expresion_numerica : PARIZQ expresion_numerica PARDER'
    t[0] = t[2]
    global gramatical 
    gramatical.append( " expresion.val : expresion.val")
def p_goto_lbl(t):
    'goto : expresion_numerica'
    t[0] = t[1]
    global gramatical 
    gramatical.append( " goto.val : expresion.val")
def p_goto(t):
    'expresion_numerica : GOTO expresion_numerica PTCOMA'
    t[0] = Goto(t[2])
    global gramatical 
    gramatical.append( " expresion.val : expresion.val")

def p_expresion_number(t):
    'expresion_numerica : ENTERO'
    t[0] = ExpresionEntero(t[1], TS.TIPO_DATO.NUMERO,t.lexer.lineno) 
    global gramatical 
    gramatical.append( " expresion.val : entero.val")
def p_expresion_decimal(t):
    'expresion_numerica : DECIMAL'
    t[0] = ExpresionEntero(t[1], TS.TIPO_DATO.FLOAT,t.lexer.lineno)
    global gramatical 
    gramatical.append( " expresion.val : decimal.val")
def p_expresion_id(t):
    'expresion_numerica   : TEMP'
    t[0] = ExpresionIdentificador(t[1])
    global gramatical 
    gramatical.append( " expresion.val : temp.val")
def p_expresion_id_labl(t):
    'expresion_numerica   : ID'
    t[0] = ExpresionIdentificador(t[1])
    global gramatical 
    gramatical.append( " expresion.val : id.val")
def p_expresion_id_param(t):
    'expresion_numerica   : PARAM'
    t[0] = ExpresionIdentificador(t[1])
    global gramatical 
    gramatical.append( " expresion.val : param.val")
def p_expresion_id_val(t):
    'expresion_numerica   : VAL'
    t[0] = ExpresionIdentificador(t[1])
    global gramatical 
    gramatical.append( " expresion.val : valor.val")
def p_expresion_id_dir(t):
    'expresion_numerica   : DIR'
    t[0] = ExpresionIdentificador(t[1])
    global gramatical 
    gramatical.append( " expresion.val : dire.val")
def p_expresion_id_pila(t):
    'expresion_numerica   : PILA'
    t[0] = ExpresionIdentificador(t[1])
    global gramatical 
    gramatical.append( " expresion.val : pila.val")
def p_expresion_id_puntero(t):
    'expresion_numerica   : PUNTERO'
    t[0] = ExpresionIdentificador(t[1])
    global gramatical 
    gramatical.append( " expresion.val : puntero.val")
def p_expresion_concatenacion(t) :
    'expresion_cadena     : expresion_cadena CONCAT expresion_cadena'
    t[0] = ExpresionConcatenar(t[1], t[3])

def p_expresion_cadena(t) :
    'expresion_numerica     : CADENA'
    t[0] = ExpresionEntero(t[1], TS.TIPO_DATO.CADENA,t.lexer.lineno)
    global gramatical 
    gramatical.append( " expresion.val : cadena.val")
def p_expresion_caracter(t):
    'expresion_numerica : CARACTER'
    t[0] = ExpresionEntero(t[1], TS.TIPO_DATO.CARACTER,t.lexer.lineno)
    global gramatical 
    gramatical.append( " expresion.val : caracter.val")
def p_expresion_cadena_numerico(t) :
    'expresion_cadena     : expresion_numerica'
    t[0] = ExpresionCadenaNumerico(t[1])

def p_expresion_arreglo(t):
    'expresion_numerica : ARRAY PARIZQ PARDER'
    t[0] = ExpresionArreglo(0,TS.TIPO_DATO.ARREGLO)
    global gramatical 
    gramatical.append( " expresion.val : arreglo.val")
def getErrores():
    #print("gramatica errores:",lista_errores)
    return lista_errores
def cleanErrores():
    
    del lista_errores[:]
    
def find_column(input, token):
     line_start = input.rfind('\n', 0, token.lexpos) + 1
     return (token.lexpos - line_start) + 1    

def p_error(t):
    #print(t)
    #print("Error sintáctico en '%s'" % t.value)
    
    while True:
        to=parser.token()
        #print("esto trae el token siguiente: ",to.type)
        if not to or to.type == 'PTCOMA' : break
        
    parser.errok()
    error = "Error sintactico en el token \'" + str(t.value) +"\' en la linea: "+ str(t.lineno) + ' columna:' + str(find_column(t.lexer.lexdata,t))
    lista_errores.append(error)
    
    
    return to
    #print(t)
    #print("Error sintáctico en '%s'" % t.value,'> ',str(t.lineno))    
def getGramatical():
    return gramatical

import ply.yacc as yacc
parser = yacc.yacc()
#print("gramatical:",gramatical)

def parse(input) :
    
    return parser.parse(input)


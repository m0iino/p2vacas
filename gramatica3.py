reservadas = {
    'printf' : 'IMPRIMIR',
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
    'exit' : 'EXIT',
    'auto' : 'AUTO',
    'break' : 'BREAK',
    'case' : 'CASE',
    'continue' : 'CONTINUE',
    'default' : 'DEFAULT',
    'do' : 'DO',
    'double' : 'DOUBLE',
    'else' : 'ELSE',
    'enum' : 'ENUM',
    'extern' : 'EXTERN',
    'for' : 'FOR',
    'register' : 'REGISTER',
    'return' : 'RETURN',
    'sizeof' : 'SIZEOF',
    'switch' : 'SWITCH',
    'struc' : 'STRUCT',
    'void' : 'VOID',
    'while' : 'WHILE'

}

tokens  = [
    'PTCOMA',
    'COMA',
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
    'PDECIMAL',
    'PSTRING',
    'PDOUBLE',
    'PCARACTER',
    
    'XORBIT',
    'MENORBIT',
    'MAYORBIT',
    'MENIGUAL',
    'MAYIGUAL'
    
] + list(reservadas.values())

# Tokens
t_PTCOMA    = r';'
t_COMA    = r','
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
t_PDECIMAL =    r'%f'
t_PCARACTER =    r'%c'
t_PDOUBLE =    r'%d'
t_PSTRING =    r'%s'
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
def t_BACKLASH(t):
    r'\\.*\n'
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
                        | definicion_variable                                         
                        | asignacion_variable
                        '''
    t[0] = t[1]
    global gramatical 
    gramatical.append( " instruccion.val: expresiones.val")

def p_instruccion_imprimir(t) :
    'imprimir_instr     : IMPRIMIR PARIZQ expresion_numerica PARDER PTCOMA'
    t[0] =Imprimir(t[3])
    global gramatical 
    gramatical.append( " imprimir.val : expresion.val")

def p_asignacion_variable(t):
    'asignacion_variable   : ID IGUAL expresion_numerica PTCOMA'
    t[0] = Asignacion(t[1], t[3])
    global gramatical 
    gramatical.append( " asignartemp.val : expresion.val")
def p_definicion_asignacion_variable(t):
    'definicion_variable : tipo lista_ids IGUAL expresion_numerica PTCOMA'
    t[0] = Definicion_Asignacion(t[1],t[2],t[4])
def p_definicion_variable(t):
    'definicion_variable : tipo lista_ids PTCOMA'
    t[0] = Definicion(t[1],t[2])
    global gramatical 
    gramatical.append( " definicion_variable.val : expresion.val")


def p_tipo(t):
    '''tipo : INT
                | FLOAT
                | DOUBLE
                | CHAR'''
    
    t[0] = t[1]

def p_lista_ids(t):
    'lista_ids : lista_ids COMA expresion_numerica'
    t[1].append(t[3])
    t[0] = t[1]
    global gramatical 
    gramatical.append( " lista_ids.val : lista_ids.append(expresion.val)")
def p_lista(t):
    'lista_ids : expresion_numerica'
    t[0] = [t[1]]
    global gramatical 
    gramatical.append( " lista_ids.val : expresion.val")
def p_lista_cad(t):
    'lista_ids : expresion_numerica CORIZQ CORDER'
    t[0] = [t[1]]
    global gramatical 
    gramatical.append( " lista_ids_cad.val : expresion.val")
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


def p_expresion_unaria(t):
    'expresion_numerica : MENOS expresion_numerica %prec UMENOS'
    t[0] = ExpresionNegativo(t[2], TS.TIPO_DATO.NUMERO)
    global gramatical 
    gramatical.append( " expresion.val : expresion.val")

def p_expresion_agrupacion(t):
    'expresion_numerica : PARIZQ expresion_numerica PARDER'
    t[0] = t[2]
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

def p_expresion_id_labl(t):
    'expresion_numerica   : ID'
    t[0] = ExpresionIdentificador(t[1],t.lexer.lineno)
    global gramatical 
    gramatical.append( " expresion.val : id.val")

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

def getErrores():
    #print("gramatica errores:",lista_errores)
    return lista_errores
def cleanErrores():
    
    del lista_errores[:]
    
def find_column(input, token):
     line_start = input.rfind('\n', 0, token.lexpos) + 1
     return (token.lexpos - line_start) + 1    

def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)
    
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


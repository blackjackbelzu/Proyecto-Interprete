from azlexico import lexico

#programa = lista_sentencias 
def programa(tokens):
    error=""
    i=0
    i,error=lista_sentencias(tokens,i)
    if error!="":
        return error
    
    if i<len(tokens):
        return f"Error sintáctico: Símbolos inesperados '{tokens[i]}' en posición {i}"

    return "Valido"

#lista_sentencias = { sentencia } 

def lista_sentencias(tokens, i):

    while i < len(tokens) and tokens[i] in (100, 101, 102, 103, 106, 107, 108, 239, 6000):
        i, error = sentencia(tokens, i)
        if error != "":
            return i, error
    return i, ""  

#sentencia = declaracion | asignacion | cambio_tipo | si | mientras | imprimir| comentario 
def sentencia(tokens,i):

    if i < len(tokens) and tokens[i] in (100, 101, 102):
        return declaracion(tokens, i)
    elif i < len(tokens) and tokens[i] == 6000:
        return asignacion(tokens, i)
    elif i < len(tokens) and tokens[i] == 108:
        return cambio_tipo(tokens, i)
    elif i < len(tokens) and tokens[i] == 103:
        return si(tokens, i)
    elif i < len(tokens) and tokens[i] == 106:
        return mientras(tokens, i)
    elif i < len(tokens) and tokens[i] == 107:
        return imprimir(tokens, i)
    elif i < len(tokens) and tokens[i] == 239:
        return comentario(tokens, i)
    else:
        return i, f"Error: Se esperaba sentencia valida '{tokens[i]}' en posicion {i}"

#declaracion =tipo lista_variables ";"
def declaracion(tokens,i):

    i,error=tipo(tokens,i)
    if error!="":
        return i,error
    
    i,error=lista_variables(tokens,i)
    if error!="":
        return i,error
    
    #;
    if i<len(tokens) and tokens[i]==235:
        i+=1
    else:
        return i, f"Error sintáctico: se esperaba ; para cerrar declaracion '{tokens[i]}' en posición {i}"

    return i,""

#tipo ="gantz"| "gleit" | "kette" 
def tipo(tokens,i):

    if i<len(tokens) and tokens[i]==100:
        i+=1
    elif i<len(tokens) and tokens[i]==101:
        i+=1
    elif i<len(tokens) and tokens[i]==102:
        i+=1
    else:
        return i, f"Error: Se esperaba iniciar con tipo de variable gantz | gleit |kette '{tokens[i]}' en posicion {i}"

    return i,""

#lista_variables = var { "," var } 
def lista_variables(tokens,i):

    if i<len(tokens) and tokens[i]==6000:
        i+=1
    else:
        return i, f"Error: Se esperaba un identificador '{tokens[i]}' en posicion {i}"

    while i<len(tokens) and tokens[i]==234:
        #,
        if i<len(tokens) and tokens[i]==234:
            i+=1
        else:
            return i, f"Error: Se esperaba ,  para listar variables '{tokens[i]}' en posicion {i}"
        
        if i<len(tokens) and tokens[i]==6000:
            i+=1
        else:
            return i, f"Error: Se esperaba un identificador despues de , '{tokens[i]}' en posicion {i}"
    
    return i,""
        
#asignacion = var "=" expresion ";" 
def asignacion(tokens,i):

    if i<len(tokens) and tokens[i]==6000:
        i+=1
    else:
        return i, f"Error: Se esperaba un identificador '{tokens[i]}' en posicion {i}"
    #=
    if i<len(tokens) and tokens[i]==220:
        i+=1
    else:
        return i, f"Error: Se esperaba = '{tokens[i]}' en posicion {i}"

    i,error=expresion(tokens,i)
    if error!="":
        return i,error

   #;
    if i<len(tokens) and tokens[i]==235:
        i+=1
    else:
        return i, f"Error sintáctico: Se esperaba ; para cerrar asignacion '{tokens[i]}' en posición {i}"

    return i,""
#cambio_tipo ="wechsel" var "=" expresion ";" 
def cambio_tipo(tokens,i):
    if i<len(tokens) and tokens[i]==108:
        i+=1
    else:
        return i, f"Error sintáctico: Se esperaba wechsel '{tokens[i]}' en posición {i}"

    if i<len(tokens) and tokens[i]==6000:
        i+=1
    else:
        return i, f"Error: Se esperaba un identificador '{tokens[i]}' en posicion {i}"
    #=
    if i<len(tokens) and tokens[i]==220:
        i+=1
    else:
        return i, f"Error: Se esperaba = '{tokens[i]}' en posicion {i}"
    
    i,error=expresion(tokens,i)
    if error!="":
        return i,error
    
    #;
    if i<len(tokens) and tokens[i]==235:
        i+=1
    else:
        return i, f"Error sintáctico: Se esperaba ; para cerrar cambio de tipo '{tokens[i]}' en posición {i}"
    
    return i,""

#expresion = termino { ("+" | "-") termino } 
def expresion(tokens,i):
    i,error=termino(tokens,i)
    if error!="":
        return i,error
    
    while i<len(tokens) and tokens[i] in (200,201):
            if i<len(tokens) and tokens[i] in (200,201):
                i+=1
            else:
                return i, f"Error: Se esperaba operador + | - '{tokens[i]}' en posicion {i}"
            i,error=termino(tokens,i)
            if error!="":
                return i,error

    return i,""

#ermino =factor { ("*" | "/" | "%") factor } 
def termino(tokens,i):
    i,error=factor(tokens,i)
    if error!="":
        return i,error
    
    while i<len(tokens) and tokens[i] in (202,203,204):
            if i<len(tokens) and tokens[i] in (202,203,204):
                i+=1
            else:
                return i, f"Error: Se esperaba operador *|/|% '{tokens[i]}' en posicion {i}"
            i,error=factor(tokens,i)
            if error!="":
                return i,error
    return i,""

#factor = var| numero | cadena | "(" expresion ")" | "-" factor 
def factor(tokens,i):
    if i<len(tokens)  and tokens[i]==6000:
        i+=1

    elif i<len(tokens) and tokens[i] in (4000,4100):
        i+=1
    #"
    elif i<len(tokens) and tokens[i]==238:
        if i<len(tokens) and tokens[i]==238:
            i,error=cadena(tokens,i)
            if error!="":
                return i,error
        else:
            return i, f"Error: Se esperaba '""' de apertura '{tokens[i]}' en posicion {i}"
    elif i<len(tokens) and tokens[i]==230:
        if i<len(tokens) and tokens[i]==230:
            i+=1
        else:
            return i, f"Error: Se esperaba ( de apertura{tokens[i]}' en posicion {i}"
        i,error=expresion(tokens,i)
        if error!="":
            return i,error
        if i<len(tokens) and tokens[i]==231:
            i+=1
        else:
            return i, f"Error: Se esperaba ) de cierre {tokens[i]}' en posicion {i}"

    elif i<len(tokens) and tokens[i]==201:
        if i<len(tokens) and tokens[i]==201:
            i+=1
        else:
            return i, f"Error: Se esperaba operador - {tokens[i]}' en posicion {i}"
        i,error=factor(tokens,i)
        if error!="":
            return i,error
    else:
        return i, f"Error: Se esperaba factor valido {tokens[i]}' en posicion {i}"
    
    return i,""
#si ="wen" "(" condicion ")" "{"lista_sentencias"}" {sinosi} [sino]
def si(tokens,i):
    if i<len(tokens) and tokens[i]==103:
        i+=1
    else:
        return i, f"Error: Se esperaba wen{tokens[i]}' en posicion {i}"
    
    if i<len(tokens) and tokens[i]==230:
        i+=1
    else:
        return i, f"Error: Se esperaba ( de apertura {tokens[i]}' en posicion {i}"
    
    i,error=condicion(tokens,i)
    if error!="":
        return i,error      
    
    if i<len(tokens) and tokens[i]==231:
        i+=1
    else:
        return i, f"Error: Se esperaba ) de cierre {tokens[i]}' en posicion {i}"

    if i<len(tokens) and tokens[i]==232:
        i+=1
    else:
        return i, f"Error: Se esperaba llave de apertura {tokens[i]}' en posicion {i}"

    i,error=lista_sentencias(tokens,i)
    if error!="":
        return i,error  
    
    if i<len(tokens) and tokens[i]==233:
            i+=1
    else:
        return i, f"Error: Se esperaba llave de cierre {tokens[i]}' en posicion {i}"

    while i<len(tokens) and tokens[i] ==105:
            i,error=sinosi(tokens,i)
            if error!="":
                return i,error
            
    if i<len(tokens) and tokens[i]==104:
            i, error = sino(tokens, i)
            if error != "":
                return i, error
    return i,""
#sinosi= "sonwen" "(" condicion ")" "{" lista_sentencias "}" 
def sinosi(tokens,i):
    if i<len(tokens) and tokens[i]==105:
        i+=1
    else:
        return i, f"Error: Se esperaba sonwen {tokens[i]}' en posicion {i}"
    
    if i<len(tokens) and tokens[i]==230:
        i+=1
    else:
        return i, f"Error: Se esperaba ( de apertura {tokens[i]}' en posicion {i}"
    
    i,error=condicion(tokens,i)
    if error!="":
        return i,error
    
    if i<len(tokens) and tokens[i]==231:
            i+=1
    else:
        return i, f"Error: Se esperaba ) de cierre {tokens[i]}' en posicion {i}"
    
    if i<len(tokens) and tokens[i]==232:
        i+=1
    else:
        return i, f"Error: Se esperaba llave de apertura {tokens[i]}' en posicion {i}"

    i,error=lista_sentencias(tokens,i)
    if error!="":
        return i,error  
    
    if i<len(tokens) and tokens[i]==233:
            i+=1
    else:
        return i, f"Error: Se esperaba llave de cierre {tokens[i]}' en posicion {i}"

    return i,""

#sino= "son" "{"lista_sentencias "}" 
def sino(tokens,i):
    if i<len(tokens) and tokens[i]==104:
        i+=1
    else:
        return i, f"Error: Se esperaba son '{tokens[i]}' en posicion {i}"  
    
    if i<len(tokens) and tokens[i]==232:
        i+=1
    else:
        return i, f"Error: Se esperaba llave de apertura {tokens[i]}' en posicion {i}"

    i,error=lista_sentencias(tokens,i)
    if error!="":
        return i,error  
    
    if i<len(tokens) and tokens[i]==233:
            i+=1
    else:
        return i, f"Error: Se esperaba llave de cierre {tokens[i]}' en posicion {i}"

    return i,""   

#mientras ="wahr" "(" condicion ")" "{"lista_sentencias"}" 
def mientras(tokens,i):
    if i<len(tokens) and tokens[i]==106:
            i+=1
    else:
        return i, f"Error: Se esperaba wahr {tokens[i]}' en posicion {i}"
    if i<len(tokens) and tokens[i]==230:
        i+=1
    else:
        return i, f"Error: Se esperaba ( de apertura {tokens[i]}' en posicion {i}"
    
    i,error=condicion(tokens,i)
    if error!="":
        return i,error
    
    if i<len(tokens) and tokens[i]==231:
            i+=1
    else:
        return i, f"Error: Se esperaba ) de cierre {tokens[i]}' en posicion {i}"
    
    if i<len(tokens) and tokens[i]==232:
        i+=1
    else:
        return i, f"Error: Se esperaba llave de apertura {tokens[i]}' en posicion {i}"

    i,error=lista_sentencias(tokens,i)
    if error!="":
        return i,error  
    
    if i<len(tokens) and tokens[i]==233:
            i+=1
    else:
        return i, f"Error: Se esperaba llave de cierre {tokens[i]}' en posicion {i}"

    return i,""   
    
#condicion = condicion_and { "oder" condicion_and }
def condicion(tokens,i):
    i,error=condicion_and(tokens,i)
    if error!="":
        return i,error  
    
    while i<len(tokens) and tokens[i] ==110:
            if i<len(tokens) and tokens[i] ==110:
                i+=1
            else:
                return i, f"Error: Se esperaba oder '{tokens[i]}' en posicion {i}"
            i,error=condicion_and(tokens,i)
            if error!="":
                return i,error
    return i,""
 
#condicion_and =condicion_simple { "und" condicion_simple} 
def condicion_and(tokens,i):
    i,error=condicion_simple(tokens,i)
    if error!="":
        return i,error  
    
    while i<len(tokens) and tokens[i] ==109:
            if i<len(tokens) and tokens[i] ==109:
                i+=1
            else:
                return i, f"Error: Se esperaba und '{tokens[i]}' en posicion {i}"
            i,error=condicion_simple(tokens,i)
            if error!="":
                return i,error
    return i,""  

#condicion_simple = "(" condicion ")" | expresion comparador expresión
def condicion_simple(tokens,i):
    
    if i < len(tokens) and tokens[i] == 230:
        if i<len(tokens) and tokens[i]==230:
            i += 1
        else:
            return  i, f"Error: Se esperaba ( de apertura '{tokens[i]}' en posicion {i}"

        i,error = condicion(tokens,i)
        if error != "":
            return i,error

        if i < len(tokens) and tokens[i] == 231:
            i += 1
        else:
            return i, f"Error: Se esperaba ) '{tokens[i]}' en posicion {i}"

        return i,""

    # expresion comparador expresion

    i,error = expresion(tokens,i)
    if error != "":
        return i,error

    elif i < len(tokens) and tokens[i] in (210,211,212,213,215,216):
        i += 1
    else:
        return i, f"Error: Se esperaba operador relacional '{tokens[i]}' en posicion {i}"

    i,error = expresion(tokens,i)
    if error != "":
        return i,error

    return i,""

#imprimir = "druck" "(" lista_impresion ")" ";" 
def imprimir(tokens,i):
    if i<len(tokens) and tokens[i] ==107:
        i+=1
    else:
        return i, f"Error: Se esperaba druck '{tokens[i]}' en posicion {i}"

    if i<len(tokens) and tokens[i]==230:
        i+=1
    else:
        return i, f"Error: Se esperaba ( de apertura{tokens[i]}' en posicion {i}"
    
    i,error=lista_impresion(tokens,i)
    if error!="":
        return i,error
    
    if i<len(tokens) and tokens[i]==231:
        i+=1
    else:
        return i, f"Error: Se esperaba ) de cierre {tokens[i]}' en posicion {i}"

    if i<len(tokens) and tokens[i]==235:
        i+=1
    else:
        return i, f"Error sintáctico: se esperaba ; para cerrar druck '{tokens[i]}' en posición {i}"
    
    return i,""
#lista_impresion = expresion { "," expresion } 
def lista_impresion(tokens,i):
    i,error=expresion(tokens,i)
    if error!="":
        return i,error
    
    while i<len(tokens) and tokens[i]==234:
        #,
        if i<len(tokens) and tokens[i]==234:
            i+=1
        else:
            return i, f"Error: Se esperaba , para listar variables '{tokens[i]}' en posicion {i}"
        i,error=expresion(tokens,i)
        if error!="":
            return i,error
        
    return i,""   
#comentario = "$" contenido_cadena 
def comentario(tokens,i):
    if i<len(tokens) and tokens[i]==239:
        i+=1
    else:
        return i, f"Error sintáctico: se esperaba $ '{tokens[i]}' en posición {i}"   
     
    if i<len(tokens) and tokens[i]==7000:
        i+=1
    else:
        return i, f"Error sintáctico: se esperaba cuerpo del comentario '{tokens[i]}' en posición {i}"   

    return i,""
#cadena = '"' contenido_cadena '"' 
def cadena(tokens,i):
    if i<len(tokens) and tokens[i]==238:
        i+=1
    else:
        return i, f"Error sintáctico: se esperaba '\"' para iniciar cadena'{tokens[i]}' en posición {i}" 
    
    if i<len(tokens) and tokens[i]==5000:
        i+=1
    else:
        return i, f"Error sintáctico: se esperaba cadena '{tokens[i]}' en posición {i}" 

    if i<len(tokens) and tokens[i]==238:
        i+=1
    else:
        return i, f"Error sintáctico: se esperaba '\"' para cerrar cadena'{tokens[i]}' en posición {i}" 

    return i,""


#INGRESO DE TOKENS POR ARCHIVO Y LLAMADA AL LEXICO
with open("cod2.txt", "r", encoding="utf-8") as archivo:
    codigo = archivo.read()

lista_tokens = lexico(codigo)

# Si el léxico devuelve un error
if isinstance(lista_tokens, str):
    print(lista_tokens)
else:
    print("\nANALIZADOR SINTACTICO RESULTADO:")
    print(programa(lista_tokens))


#INGRESO DE TOKENS MANUAL
'''
lista_tokens=[239, 7000, 102, 6000, 235, 100, 6000, 235, 
              101, 6000, 235, 6000, 220, 238, 5000, 238, 235, 107, 230, 238, 5000, 238, 234, 6000, 231, 235, 108, 6000, 220, 
              4000, 235, 6000, 220, 6000, 200, 4000, 235, 107, 230, 238, 
              5000, 238, 234, 6000, 231, 235, 108, 6000, 220, 4100, 235, 6000, 220, 6000, 202, 4000, 235, 107, 230, 238, 5000, 238, 234, 6000, 231, 235, 239, 7000, 100, 6000, 234, 6000, 235, 102, 6000, 235, 6000, 220, 4000, 235, 6000, 220, 4000, 235, 103, 230, 230, 6000, 215, 4000, 231, 109, 230, 6000, 213, 4000, 231, 231, 232, 6000, 220, 238, 5000, 238, 235, 233, 105, 230, 230, 6000, 215, 4000, 231, 109, 230, 6000, 213, 4000, 231, 231, 232, 6000, 220, 238, 5000, 238, 235, 233, 105, 230, 230, 6000, 211, 4000, 231, 109, 230, 6000, 213, 4000, 231, 231, 232, 6000, 220, 238, 5000, 238, 235, 233, 104, 232, 6000, 220, 238, 5000, 238, 235, 233, 107, 230, 238, 5000, 238, 234, 6000, 231, 235]
print(programa(lista_tokens))
'''
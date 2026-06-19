def lexico(codigo):
    
    codigo = codigo + "\n"
    token = []

    i = 0
    n = len(codigo)

    estado = 0
    palabra = ""
    tipo_comilla=""

    while i < n:
        c = codigo[i]

        # ESTADO INICIAL
        if estado == 0:

            # ESPACIOS
            if c.isspace():
                i += 1
                continue

            # IDENTIFICADORES
            elif c.isalpha():
                palabra = c
                i += 1
                estado = 6000
                continue

            # NUMEROS
            elif c.isdigit():
                palabra = c
                i += 1
                estado = 4000
                continue
            #CADENA
            elif c=='"':
                i+=1
                estado=238
                tipo_comilla="apertura"
                continue
            #operadores aritmeticos
            elif c=="+":
                i+=1
                estado=200
                continue
            elif c=="-":
                i+=1
                estado=201
                continue
            elif c=="*":
                i+=1
                estado=202
                continue
            elif c=="/":
                i+=1
                estado=203
                continue
            elif c=="%":
                i+=1
                estado=204
                continue
            #operadores relacionales/Asignacion
            elif c=="<":
                i+=1
                estado=-3
                continue
            elif c==">":
                i+=1
                estado=-4
                continue
            #asignacion
            elif c=="=":
                i+=1
                estado=-6
                continue
            #simbolos especiales
            elif c=="(":
                i+=1
                estado=230
                continue
            elif c==")":
                i+=1
                estado=231
                continue
            elif c=="{":
                i+=1
                estado=232
                continue
            elif c=="}":
                i+=1
                estado=233
                continue
            elif c==",":
                i+=1
                estado=234
                continue
            elif c==";":
                i+=1
                estado=235
                continue
            elif c=="$":
                i+=1
                estado=239
                continue

            else:
                return f"Error caracter invalido '{c}' posicion={i}"

        # IDENTIFICADORES
        elif estado == 6000:

            if c.isalnum() or c == "_":
                palabra += c
                i += 1
                continue

            else:
                estado=-20
        elif estado==-20:
            # PALABRAS RESERVADAS
                reservadas = {
                    "gantz":100,
                    "gleit":101,
                    "kette":102,
                    "wen":103,
                    "son":104,
                    "sonwen":105,
                    "wahr":106,
                    "druck":107,
                    "wechsel":108,
                    "und":109,
                    "oder":110
                }

                if palabra.lower() in reservadas:
                    token.append(reservadas[palabra])
                else:
                    token.append(6000) # IDENTIFICADOR

                palabra = ""
                estado = 0
                continue        

        # ENTERO
        elif estado == 4000:
            if c.isdigit():
                palabra += c
                i += 1
                continue

            elif c == ".":
                palabra += c
                i += 1
                estado = -1
                continue

            elif c.isalpha() or c == "_":
                    return "Error léxico: identificador debe comenzar con una letra"

            else:
                if len(palabra) > 1 and palabra[0] == "0":
                    return "Error léxico: número entero no puede iniciar con cero"

                token.append(4000)
                palabra = ""
                estado = 0
                continue

        # PARTE DECIMAL
        elif estado == -1:

            if c.isdigit():
                palabra += c
                i += 1
                estado = 4100
                continue
            elif c.isalpha() or c == "_":
                return "Error léxico: identificador debe comenzar con una letra "
            else:
                return  f"Error léxico: número decimal inválido'"

        # REAL
        elif estado == 4100:
            if c.isdigit():
                palabra += c
                i += 1
                continue
            else:
                parte_entera = palabra.split(".")[0]

                if len(parte_entera) > 1 and parte_entera[0] == "0":
                    return "Error léxico: ceros a la izquierda no permitidos"
                token.append(4100)
                palabra = ""
                estado = 0
                continue
        elif estado==238:
            token.append(238)   # comilla de apertura
            if tipo_comilla=="apertura":
                estado = 5000
            else: #cierre
                estado=0
            continue
        elif estado==5000:
            if c=='"':
                token.append(5000)
                i+=1
                tipo_comilla="cierre"
                estado=238
                continue
            elif c=="\n":
                return "Error léxico: cadena no cerrada"
            elif c.isalnum() or c in "()+-*/%<>=!? _.,:;\t":
                palabra=palabra+c
                i+=1
                continue
            else:
                return f"Error léxico: carácter no permitido en cadena '{c}'"
        elif estado in (200,201,202,203,204,210,211,212,213,214,215,216,220,
                        230,231,232,233,234,235):
            token.append(estado)
            estado=0
            continue
        elif estado==-3: #Viene de "<"
            if c==">":   #<> diferente
                i+=1
                estado=210
                continue
            elif c=="=": #<=
                i+=1
                estado=216
                continue
            else:
                # <
                estado=211
                continue
        elif estado==-4: #Viene de ">"
            if c=="=": #>=
                i+=1
                estado=215
                continue
            else:
                #>
                estado=212
                continue
        elif estado==-6: #Viene de un "="
            if c=="=": #==
                i+=1
                estado=213
                continue
            else:
                #=
                estado=220
                continue
        elif estado==239:
                token.append(239)
                estado=7000
                continue      
        elif estado==7000:
            if c=="\n":
                estado=-10
                continue
            else:
                palabra=palabra+c
                i+=1
                continue
        elif estado==-10:
            token.append(7000)
            palabra=""
            estado=0
            continue
    if estado == 5000:
        return "Error léxico: cadena no cerrada"
    
    return token


#TRADUCCION DE CODIGO FUENTE A TOKENS POR ARCHIVO
try:
    with open("cod2.txt", "r", encoding="utf-8") as archivo:
        codigo_fuente = archivo.read()

    print("Código fuente leído:\n")
    print(codigo_fuente)

    print("\nLista de Tokens generada:")
    print(lexico(codigo_fuente))

except FileNotFoundError:
    print("Error: no se encontró el archivo programa.txt")

except Exception as e:
    print(f"Error al leer el archivo: {e}")   
            

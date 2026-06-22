
def infposf(expresion):
    precedencia = {"+":1,"-":1,
                    "*":2,"/":2,"%":2,
                    "^":3
    }

    asociatividad_derecha = {"^"}

    pila = []
    salida = []

    tokens = separar(expresion)

    for token in tokens:
        #si token es un identificador
        if es_operando(token):
            salida.append(token)
        elif token == "(":
            pila.append(token)
        elif token == ")":

            while pila and pila[-1] != "(":
                salida.append(pila.pop())
            if not pila:
                return "Error semántico: ')' sin '(' correspondiente."

            pila.pop()
        else:
            while (pila  and  pila[-1] != "("  and
                (precedencia[pila[-1]] > precedencia[token]  or
                    (precedencia[pila[-1]]== precedencia[token]  and
                     token not in asociatividad_derecha
                    )
                )
            ):
                salida.append(pila.pop())
            pila.append(token)
    while pila:
        if pila[-1] == "(":
            return "Error semántico: falta ')' de cierre."
        salida.append(pila.pop())
    return salida



# SEPARAR TOKENS
def separar(expresion):

    tokens = []
    palabra = ""
    operadores = "+-*/%^()"
    for c in expresion:
        if c == " ":
            if palabra:
                tokens.append(palabra)
                palabra = ""

        elif c in operadores:
            if palabra:
                tokens.append(palabra)
                palabra = ""
            tokens.append(c)
        else:
            palabra += c

    if palabra:
        tokens.append(palabra)
    return tokens


# OPERANDO
def es_operando(token):
    return token not in [
        "+","-","*","/","%","^",
        "(",")"
    ]

#CUARTETOS
def genCuarteto(postfija):
    pila = []
    cuartetos = []
    temp = 1
    operadores = {
        "+","-","*","/","%","^"
    }

    for token in postfija:
        if token not in operadores:
            pila.append(token)
        else:
            if len(pila) < 2:
                return "Error semántico: operador '{}' sin suficientes operandos.".format(token)

            op2 = pila.pop()
            op1 = pila.pop()
            temporal = f"T{temp}"
            cuartetos.append((token,op1,op2,temporal))

            pila.append(temporal)
            temp += 1
    if len(pila) != 1:
        return "Error semántico: expresión inválida."
    
    return cuartetos

# TERCETOS
def genTerceto(postfija):

    pila = []
    tercetos = []
    contador = 1
    operadores = {
        "+","-","*","/","%","^"
    }

    for token in postfija:
        if token not in operadores:
            pila.append(token)
        else:
            if len(pila) < 2:
                return "Error semántico: operador '{}' sin suficientes operandos.".format(token)
            op2 = pila.pop()
            op1 = pila.pop()
            tercetos.append((token,op1,op2))
           
            pila.append(
                f"({contador})"
            )
            contador += 1

    if len(pila) != 1:
        return "Error semántico: expresión inválida."

    return tercetos     

# EXTRAER ASIGNACIONES
def obtener_asignaciones(codigo):

    asignaciones = []
    lineas = codigo.split("\n")

    for linea in lineas:
        linea = linea.strip()

        if not linea:
            continue

        if "==" in linea:
            continue

        if "<>" in linea:
            continue

        if "<=" in linea:
            continue

        if ">=" in linea:
            continue

        if "wen" in linea:
            continue

        if "=" not in linea:
            continue

        partes = linea.split(";")

        for parte in partes:
            parte = parte.strip()
            if "=" not in parte:
                continue
            izquierda, derecha = parte.split("=",1)
            variable = izquierda.strip()
            expresion = derecha.strip()
            asignaciones.append((variable,expresion))

    return asignaciones


def semantico(codigo):
    
    asignaciones = obtener_asignaciones(codigo)

    print("\nANALISIS SEMANTICO:")
    if len(asignaciones) == 0:
        print("No existen asignaciones.")
        return "Valido"
    for variable, expresion in asignaciones:
        print("\n-------------------")
        print("Infija")
        print(variable, "=", expresion)
        operadores = ["+","-","*","/","%","^"]

        if not any(
            op in expresion
            for op in operadores
        ):

            print("No genera representacion intermedia." )
            continue

        postfija = infposf(expresion)
        if isinstance(postfija, str):
            return postfija
        print("\nPOSTFIJA:")
        print("".join(postfija))
        print("\nCUARTETOS:")
        cuartetos = genCuarteto(postfija)
        if isinstance(cuartetos, str):
            return cuartetos
        for i, c in enumerate(cuartetos,start=1):

            print(i,":",c)
        print("\nTERCETOS:")
        tercetos = genTerceto(postfija)
        if isinstance(tercetos, str):
            return tercetos
        for i, t in enumerate(tercetos,start=1):
            print(i,":",t)
    return "Valido"

if __name__ == "__main__":
    
    archivo = input("Ingrese el nombre del archivo(Ejemplo: cod.txt): ")

    try:
        with open(archivo,"r", encoding="utf-8" ) as f:
            codigo = f.read()
        resultado = semantico(codigo)
        if resultado != "Valido":
            print(resultado)
        else:
            print("Analisis semantico valido.")
    except FileNotFoundError:
        print("Archivo no encontrado.")
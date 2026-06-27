from azlexico import lexico

# Para convertir de infijo a posfijo
def infposf(tokens):
    # precedencia
    prec = {109: -1, 110: -1, 211: 0, 212: 0, 213: 0, 215: 0, 
            216: 0, 210: 0, 200: 1, 201: 1, 202: 2, 203: 2, 204: 2}
    pila, salida = [], []
    for token, lexema in tokens: # si es num, ident y cadena
        if token in (4000, 4100, 5000, 6000): 
            salida.append((token, lexema))
        elif token == 230: 
            pila.append((token, lexema))
        elif token == 231:
            while pila and pila[-1][0] != 230: 
                salida.append(pila.pop())
            if pila: 
                pila.pop()
        elif token in prec:
            while (pila and pila[-1][0] != 230 and 
                    prec.get(pila[-1][0], -2) >= prec[token]): 
                        salida.append(pila.pop())
            pila.append((token, lexema))
    while pila: 
        salida.append(pila.pop())
    return salida

ENTORNO = {"t": 1, "l": 1, "e": 1, "c": 1} # Almacena Cuarteto T, Etiqueta L, Terceto c
PILA_BLOQUES, ETIQUETAS_FIN = [], [] # controla estructuras de control

# Tabla de simbolos para imprimir las instrucciones
TABLA_INVERSA = {
    100: "gantz", 101: "gleit", 102: "kette", 103: "wen", 
    104: "son", 105: "sonwen", 106: "wahr", 107: "druck",
    108: "wechsel", 109: "und", 110: "oder", 200: "+", 201: "-", 
    202: "*", 203: "/", 204: "%", 210: "<>",
    211: "<", 212: ">", 213: "==", 215: ">=", 216: "<=", 220: 
    "=", 230: "(", 231: ")", 232: "{", 233: "}",
    234: ",", 235: ";", 238: '"', 239: "$"
}

# Generar Cuartetos
def genCuarteto(postfija, destino=None, es_condicion=False, tipo_control="wen"):
    pila_c, cuartetos = [], []
    for token, lexema in postfija:
        if token not in {200, 201, 202, 203, 204, 210, 211, 212, 213, 215, 216, 109, 110}: 
            pila_c.append(lexema)
        else:
            if len(pila_c) < 2: 
                return [], "_"
            op2 = pila_c.pop()
            op1 = pila_c.pop()
            temp_var = f"T{ENTORNO['t']}"
            cuartetos.append((TABLA_INVERSA.get(token, "?"), op1, op2, temp_var))
            pila_c.append(temp_var)
            ENTORNO['t'] += 1
    if es_condicion:
        etq_falso = f"L{ENTORNO['e']}"
        cuartetos.append((f"{tipo_control} es falso", pila_c[0] if pila_c else "_", "_", etq_falso))
        ENTORNO['e'] += 1 
        return cuartetos, etq_falso
    if destino and pila_c: 
        cuartetos.append(("=", pila_c[0], "_", destino))
    return cuartetos, None

# Generar Tercetos para Expresiones Matemáticas / Condicionales
def genTerceto(postfija, destino=None):
    pila_t, tercetos = [], []
    for token, lexema in postfija:
        if token not in {200, 201, 202, 203, 204, 210, 211, 212, 213, 215, 216, 109, 110}: 
            pila_t.append(lexema)
        else:
            if len(pila_t) < 2: 
                return []
            op2 = pila_t.pop()
            op1 = pila_t.pop()
            tercetos.append((TABLA_INVERSA.get(token, "?"), op1, op2))
            ref = f"({ENTORNO['c']})"
            pila_t.append(ref)
            ENTORNO['c'] += 1
    if destino and pila_t:
        tercetos.append(("=", destino, pila_t[0]))
        ENTORNO['c'] += 1
    return tercetos, pila_t[0] if pila_t else "_"

def unir_lexemas(tokens_numericos, codigo_fuente):
    tokens_con_lexema, i, n = [], 0, len(codigo_fuente)
    for tok in tokens_numericos:
        while i < n and codigo_fuente[i].isspace(): i += 1
        if i >= n: break
        if tok in TABLA_INVERSA:
            tokens_con_lexema.append((tok, TABLA_INVERSA[tok]))
            i += len(TABLA_INVERSA[tok])
        elif tok in (4000, 4100, 5000, 6000, 7000):
            lex = ""
            if tok == 5000:
                while i < n and codigo_fuente[i] != '"': 
                    lex += codigo_fuente[i]; i += 1
                lex = lex.strip()
            else:
                while i < n and (codigo_fuente[i].isalnum() or codigo_fuente[i] in "._"): 
                    lex += codigo_fuente[i]
                    i += 1
            tokens_con_lexema.append((tok, lex))
    return tokens_con_lexema

def imprimir_expresiones(cond_tokens, postfija):
    inf = "".join([t[1] for t in cond_tokens]).strip()
    pos = "".join([t[1] for t in postfija]).strip()
    print(f"  • Conversión Postfija\nInfijo: {inf} \nPostfijo: {pos}")

def ejecucion_semantica_por_bloques(tokens_planos, codigo_fuente):
    global PILA_BLOQUES, ETIQUETAS_FIN
    PILA_BLOQUES, ETIQUETAS_FIN = [], []
    ENTORNO["t"], ENTORNO["l"], ENTORNO["e"], ENTORNO["c"] = 1, 1, 1, 1
    lineas_tokens, linea_actual = [], []
    for t in unir_lexemas(tokens_planos, codigo_fuente):
        linea_actual.append(t)
        if t[0] in (235, 232, 233): 
            lineas_tokens.append(linea_actual); linea_actual = []
    if linea_actual: 
        lineas_tokens.append(linea_actual)

    print("\nANÁLISIS SEMÁNTICO")
    for lt in lineas_tokens:
        ids, lexemas = [t[0] for t in lt], [t[1] for t in lt]
        
        # ----------------- FIN DE BLOQUE ( } ) -----------------
        if ids[0] == 233 and len(ids) == 1:
            if PILA_BLOQUES:
                b = PILA_BLOQUES.pop()
                print(f"\n[Fin de Bloque]: {{ ({b['tipo'].upper()})\n" + "-"*40 + "\n  • Conversión Postfija -> Ninguno")
                
                if b["tipo"] == "wahr": 
                    print(f"  • Retorno al ciclo -> ('GOTO', '{b['inicio']}')\n  • Cierre del ciclo  -> (LABEL, {b['falso']})")
                    print(f"  • Terceto de Retorno-> {ENTORNO['c']} : ('GOTO', '{b['inicio_terceto']}', '_')")
                    ENTORNO['c'] += 1
                    print(f"  • Terceto de Cierre -> {ENTORNO['c']} : ('LABEL', '{b['falso_terceto']}', '_')")
                    ENTORNO['c'] += 1
                elif b["tipo"] == "son":
                    while ETIQUETAS_FIN:
                        lbl, lbl_t = ETIQUETAS_FIN.pop()
                        print(f"  • Despliegue Etiqueta de Fin -> (LABEL, {lbl})")
                        print(f"  • Terceto Despliegue Fin     -> {ENTORNO['c']} : ('LABEL', '{lbl_t}', '_')")
                        ENTORNO['c'] += 1
            continue
            
        # ----------------- DECLARACIONES -----------------
        if ids[0] in (100, 101, 102): 
            print(f"\n[Declaración]: {' '.join(lexemas)}\n" + "-"*40 + f"\n  • Conversión Postfija -> Ninguno\n  • Tipo       ->  {lexemas[0].capitalize()}")
            
        # ----------------- ESTRUCTURAS WEN / SONWEN / WAHR -----------------
        elif any(k in ids for k in (103, 105, 106)):
            tipo = "wahr" if 106 in ids else ("sonwen" if 105 in ids else "wen")
            print(f"\n[Estructura de Control]: {' '.join(lexemas)}\n" + "-"*40)
            
            etq_ini, t_etq_ini = None, None
            if tipo == "wahr": 
                etq_ini = f"L{ENTORNO['e']}"
                t_etq_ini = f"LT{ENTORNO['e']}"
                ENTORNO['e'] += 1
                print(f"  • Etiqueta de Retorno -> (LABEL, {etq_ini})")
                print(f"  • Terceto de Retorno  -> {ENTORNO['c']} : ('LABEL', '{t_etq_ini}', '_')")
                ENTORNO['c'] += 1
                
            if tipo == "sonwen":
                etq_fin = f"L{ENTORNO['e']}"
                t_etq_fin = f"LT{ENTORNO['e']}"
                ENTORNO['e'] += 1
                ETIQUETAS_FIN.append((etq_fin, t_etq_fin))
                print(f"  • Salto de escape rama anterior -> ('GOTO', '{etq_fin}')")
                print(f"  • Terceto Salto rama anterior   -> {ENTORNO['c']} : ('GOTO', '{t_etq_fin}', '_')")
                ENTORNO['c'] += 1
                if PILA_BLOQUES: 
                    b_ant = PILA_BLOQUES.pop()
                    print(f"  • Cierre de la condición anterior -> (LABEL, {b_ant['falso']})")
                    print(f"  • Terceto Cierre cond. anterior   -> {ENTORNO['c']} : ('LABEL', '{b_ant['falso_terceto']}', '_')")
                    ENTORNO['c'] += 1

            idx_a, idx_c = ids.index(230), len(ids) - ids[::-1].index(231) - 1
            cond = lt[idx_a+1:idx_c]; post = infposf(cond); imprimir_expresiones(cond, post)
            
            cuartetos, etq_f = genCuarteto(post, es_condicion=True, tipo_control=tipo)
            t_etq_f = f"LT{ENTORNO['e']-1}" # Reutiliza el índice de la etiqueta correspondiente
            
            tercetos_cond, ult_ref = genTerceto(post)
            tercetos_cond.append((f"{tipo} es falso", ult_ref, t_etq_f))
            t_idx_cond_falsa = ENTORNO['c']
            ENTORNO['c'] += 1

            print("  • Cuartetos generados:"); [print(f"      {c}") for c in cuartetos]
            print("  • Tercetos generados:"); [print(f"      {i} : {t}") for i, t in enumerate(tercetos_cond, t_idx_cond_falsa - len(tercetos_cond) + 1)]
            
            PILA_BLOQUES.append({
                "tipo": tipo, 
                "inicio": etq_ini, "inicio_terceto": t_etq_ini, 
                "falso": etq_f, "falso_terceto": t_etq_f
            })
            
        # ----------------- ESTRUCTURA SON -----------------
        elif 104 in ids:
            print(f"\n[Estructura de Control]: {' '.join(lexemas)}\n" + "-"*40 + "\n  • Conversión Postfija -> Ninguno")
            etq_fin = f"L{ENTORNO['e']}"
            t_etq_fin = f"LT{ENTORNO['e']}"
            ENTORNO['e'] += 1
            ETIQUETAS_FIN.append((etq_fin, t_etq_fin))
            print(f"  • Salto de escape rama anterior -> ('GOTO', '{etq_fin}')")
            print(f"  • Terceto Salto rama anterior   -> {ENTORNO['c']} : ('GOTO', '{t_etq_fin}', '_')")
            ENTORNO['c'] += 1
            if PILA_BLOQUES: 
                b_ant = PILA_BLOQUES.pop()
                print(f"  • Cierre rama condicional anterior -> (LABEL, {b_ant['falso']})")
                print(f"  • Terceto Cierre cond. anterior     -> {ENTORNO['c']} : ('LABEL', '{b_ant['falso_terceto']}', '_')")
                ENTORNO['c'] += 1
            PILA_BLOQUES.append({"tipo": "son", "falso": None, "falso_terceto": None})
            
        # ----------------- INSTRUCCIÓN DRUCK -----------------
        elif 107 in ids:
            idx_a, idx_c = ids.index(230), len(ids) - ids[::-1].index(231) - 1
            contenido = ''.join(lexemas[idx_a+1:idx_c]).strip()
            print(f"\n[Instrucción]: {' '.join(lexemas)}\n" + "-"*40 + f"\n  • Conversión Postfija -> Ninguno")
            print(f"  • Cuartetos generados:\n      1 : ('druck', '{contenido}', '_', '_')")
            print(f"  • Tercetos generados:\n      {ENTORNO['c']} : ('druck', '{contenido}', '_')")
            ENTORNO['c'] += 1
            
        # ----------------- ASIGNACIONES ( = ) -----------------
        elif 220 in ids:
            v_dest = lexemas[ids.index(220) - 1]; exp = lt[ids.index(220) + 1 : -1]; post = infposf(exp)
            print(f"\n[Instrucción]: {' '.join(lexemas)}\n" + "-"*40); imprimir_expresiones(exp, post)
            
            cuartetos, _ = genCuarteto(post, destino=v_dest, es_condicion=False)
            
            t_idx_inicio = ENTORNO['c']
            tercetos, _ = genTerceto(post, destino=v_dest)
            
            print("  • Cuartetos generados:"); [print(f"      {i} : {c}") for i, c in enumerate(cuartetos, 1)]
            print("  • Tercetos generados:"); [print(f"      {i} : {t}") for i, t in enumerate(tercetos, t_idx_inicio)]
            
        if ids[-1] == 233 and PILA_BLOQUES and PILA_BLOQUES[-1]["tipo"] == "son":
            PILA_BLOQUES.pop()
            while ETIQUETAS_FIN: 
                lbl, lbl_t = ETIQUETAS_FIN.pop()
                print(f"  • Despliegue Etiqueta de Fin -> (LABEL, {lbl})")
                print(f"  • Terceto Despliegue Fin     -> {ENTORNO['c']} : ('LABEL', '{lbl_t}', '_')")
                ENTORNO['c'] += 1


def semantico(tokens_planos, codigo_fuente):
    try:
        ejecucion_semantica_por_bloques(tokens_planos, codigo_fuente)
        return "Valido"
    except Exception as e:
        return f"Error en el análisis semántico: {str(e)}"

if __name__ == "__main__":
    try:
        with open(input("Ingrese el nombre del archivo(Ejemplo: cod.txt): "), "r", encoding="utf-8") as f: src = f.read()
        res = lexico(src)
        if isinstance(res, str): 
            print(res)
        else: 
            ejecucion_semantica_por_bloques(res, src)
    except FileNotFoundError: print("Error: archivo no encontrado.")
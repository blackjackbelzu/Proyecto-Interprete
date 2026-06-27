from azlexico import lexico
from azsintactico import programa
from azsemantico import semantico

while True:
    print("\n-----------------------------------------------")
    print("ANALISIS DE PROGRAMAS DEL INTERPRETE ALCHEMISTGOLD")
    print("--------------------------------------------------")
    print("FASES PRELIMINARES PARA GENERAR CODIGO INTERMEDIO")

    archivo = input("Ingrese el nombre del archivo(Ejemplo: cod.txt): ")

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            codigo = f.read()
    except FileNotFoundError:
        print("\nERROR: El archivo no existe.")
    else:

        # 1. ANALISIS LEXICO
        print("\nANALISIS LEXICO")
        print("----------------------------------------")
        tokens = lexico(codigo)

        if isinstance(tokens, str):
            print(tokens) # Muestra el error si el léxico falló
        else:
            print("\nTokens generados (IDs):")
            print(tokens)
            print("» Análisis léxico  valido.")


            # 2. ANALISIS SINTACTICO
            print("\nANALISIS SINTACTICO")
            resultado = programa(tokens)

            if resultado != "Valido":
                print(resultado)
            else:
                print("Analisis sintactico valido.")

                # 3. ANALISIS SEMANTICO
                # Le pasamos la lista de enteros 'tokens' y el 'codigo' fuente
                resultado = semantico(tokens, codigo)

                if resultado != "Valido":
                    print(resultado)
                else:
                    print("\nAnalisis semantico valido.")

    respuesta = input("\nDesea analizar otro archivo (S/N): ")

    if respuesta.upper() != "S":
        break
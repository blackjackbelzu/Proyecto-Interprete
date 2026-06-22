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

        # ANALISIS LEXICO
        print("\nANALISIS LEXICO")
        tokens = lexico(codigo)

        if isinstance(tokens, str):
            print(tokens)
        else:
            print(tokens)

            # ANALISIS SINTACTICO
            print("\nANALISIS SINTACTICO")
            resultado = programa(tokens)

            if resultado != "Valido":
                print(resultado)
            else:
                print("Analisis sintactico valido.")

                # ANALISIS SEMANTICO
                resultado = semantico(codigo)

                if resultado != "Valido":
                    print(resultado)
                else:
                    print("Analisis semantico valido.")

    respuesta = input("\nDesea analizar otro archivo (S/N): ")

    if respuesta.upper() != "S":
        break
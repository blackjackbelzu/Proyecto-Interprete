# Proyecto Desarrollo de un Intérprete para el lenguaje AlchemistGold

Proyecto desarrollado para la materia de Compiladores.

Este proyecto implementa un intérprete para un lenguaje de Alchemist, incluyendo:

- Analizador Léxico
- Analizador Sintáctico 
- Analizador Semántico
- codigos fuente de prueba
- Manejo de errores 

## Estructura del proyecto

```
Proyecto-Interprete/
│
├── azlexico.py          # Analizador léxico
├── sintactico.py        # Analizador sintáctico
├── cod1.txt             # Código fuente de prueba
├── cod2.txt             # Código fuente de prueba
├── cod3.txt             # Código fuente de prueba
└── README.md
```

## Requisitos

- Python 3.13.7

Verificar la instalación:

```bash
python --version
```

## Instalación

### 1. Si desea Clonar el repositorio
- Instale Visual Studio Code en su maquina
- Instale Git en su maquina
- Registrese en GitHub
- Instale Extension Python Visual Studio Code
- Abra una terminal en una carpeta cualquiera
- Realize el siguiente comando 
```bash
git clone https://github.com/blackjackbelzu/Proyecto-Interprete.git
```

### 2. Entrar al proyecto

```bash
cd Proyecto-Interprete
```

## Ejecución
Cree o Edite el archivo texto plano suministrado con su extension "nombre del archivo.txt"
```
cod2.txt
```
con el programa que se desea analizar.

Ingrese el nombre del archivo en la linea 515 en el archivo azsintactico.py:
with open("cod1.txt", "r", encoding="utf-8") as archivo:

Luego ejecutar

```bash
python azsintactico.py
```

El programa ejecutará automáticamente:

1. Analizador Léxico
2. Analizador Sintáctico

Mostrando los tokens generados y el resultado del análisis. Ademas de errores que pueda tener el codigo.

## Lenguaje soportado

El lenguaje implementa:

- Declaración de variables
- Asignaciones
- Cambio de tipo (`wechsel`)
- Condicionales (`wen`, `sonwen`, `son`)
- Ciclos (`wahr`)
- Impresión (`druck`)
- Comentarios (`$`)
- Expresiones aritméticas
- Expresiones lógicas

## Ejemplo

```txt
gantz x;

x = 5;

druck("Valor:", x);
```

## Autores

- Gustavo Belzu Rios 
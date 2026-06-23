# PROYECTO DESARROLLO DE UN INTÉRPRETE PARA EL LENGUAJE ALCHEMISTGOLD

Proyecto desarrollado para la asignatura de Compiladores.

El objetivo del proyecto es implementar las fases preliminares de un
intérprete para el lenguaje AlchemistGold, realizando el análisis de un
programa fuente hasta la generación de su representación intermedia.

## CARACTERÍSTICAS

El proyecto implementa las siguientes fases:

- Análisis Léxico
- Análisis Sintáctico
- Análisis Semántico
- Conversión de expresiones infijas a postfijas
- Generación de Cuartetos
- Generación de Tercetos
- Detección y reporte de errores léxicos, sintácticos y semánticos

## ESTRUCTURA DEL PROYECTO

```text
Proyecto-Interprete/
│
├── azlexico.py           Analizador Léxico
├── azsintactico.py       Analizador Sintáctico
├── azsemantico.py        Analizador Semántico
├── main.py               Programa Principal
│
├── cod1.txt              Programa de prueba
├── cod2.txt              Programa de prueba
├── cod3.txt              Programa de prueba
│
├── ejemplos_lexico.txt
├── ejemplos_sintactico.txt
├── ejemplos_semantica.txt
│
├── error1.txt            Programa con errores
│
└── README.md
```

## REQUISITOS

- Python 3.13 o superior

Verificar instalación:

python --version

## INSTALACIÓN

1. Clonar el repositorio

git clone https://github.com/blackjackbelzu/Proyecto-Interprete.git

2. Ingresar al proyecto

cd Proyecto-Interprete

No es necesario instalar librerías adicionales.

## EJECUCIÓN

Ejecutar el programa principal:

```bash
python main.py
```

El sistema solicitará el nombre del archivo a analizar.

Ejemplo:

Ingrese el nombre del archivo (Ejemplo: cod.txt):

cod2.txt

Luego preguntará si desea analizar otro archivo.

Desea analizar otro archivo (S/N):

## EJECUCIÓN SOLITARIA DE LOS PROGRAMAS

Ejecutar el programa principal:
```bash
python azlexico.py 
```

```bash
python azsintactico.py
```

```bash
python azsemantico.py 
```

El sistema solicitará el nombre del archivo a analizar.

Ejemplo:

Ingrese el nombre del archivo (Ejemplo: cod.txt):

cod3.txt

Luego preguntará si desea analizar otro archivo.

Desea analizar otro archivo (S/N):

## FLUJO DEL INTÉRPRETE

```text
Código Fuente
      │
      ▼
Análisis Léxico
      │
      ▼
Análisis Sintáctico
      │
      ▼
Análisis Semántico
      │
      ▼
Conversión Infija → Postfija
      │
      ▼
Generación de Cuartetos
      │
      ▼
Generación de Tercetos
```

## ANÁLISIS LÉXICO

Durante esta fase se identifican:

- Palabras reservadas
- Identificadores
- Números enteros
- Números reales
- Cadenas
- Operadores aritméticos
- Operadores relacionales
- Operadores de asignación
- Símbolos especiales
- Comentarios

Además detecta errores como:

- Caracteres inválidos
- Cadenas no cerradas
- Números mal formados
- Identificadores inválidos

## ANÁLISIS SINTÁCTICO

El analizador sintáctico verifica que el programa cumpla con la
gramática definida mediante un parser descendente recursivo.

Reconoce estructuras como:

- Declaraciones
- Asignaciones
- Cambio de tipo
- Expresiones aritméticas
- Condicionales
- Ciclos
- Impresión
- Comentarios

## ANÁLISIS SEMÁNTICO

Durante esta etapa se realiza:

- Conversión de expresiones infijas a postfijas
- Generación de Cuartetos
- Generación de Tercetos
- Validación de expresiones
- Detección de errores semánticos

## LENGUAJE ALCHEMISTGOLD

Tipos de datos

gantz
gleit
kette

Sentencias soportadas

- Declaración de variables
- Asignación
- Cambio de tipo (wechsel)
- Condicional (wen)
- Else If (sonwen)
- Else (son)
- Ciclo (wahr)
- Impresión (druck)
- Comentarios ($)

## EJEMPLO DE CÓDIGO

gantz a, b;
gleit x;
kette mensaje;

a = 10;
b = 20;

wen (a < b) {

    druck("A es menor");

}

son {

    druck("A no es menor");

}

x = (a + b) * 3;

wechsel mensaje = "Proceso terminado";

## ARCHIVOS DE PRUEBA

cod1.txt
Programa válido.

cod2.txt
Programa válido.

cod3.txt
Programa válido.

error1.txt
Programa con errores.

ejemplos_lexico.txt
Ejemplos para el análisis léxico.

ejemplos_sintactico.txt
Ejemplos para el análisis sintáctico.

ejemplos_semantica.txt
Ejemplos para el análisis semántico.

## SALIDA DEL PROGRAMA

ANALISIS LEXICO

[100, 6000, 235, ...]

ANALISIS SINTACTICO

Analisis sintactico valido.

## ANALISIS SEMANTICO

Infija:
x = a + b * c

POSTFIJA:
abc*+

CUARTETOS

1 : (*, b, c, T1)
2 : (+, a, T1, T2)

TERCETOS

1 : (*, b, c)
2 : (+, a, (1))

Analisis semantico valido.

## TECNOLOGÍAS UTILIZADAS

- Python 3.13.7
- Parser Descendente Recursivo
- Autómata Finito Determinista (AFD)
- Conversión Infija → Postfija
- Representación Intermedia mediante Cuartetos
- Representación Intermedia mediante Tercetos

## AUTOR

Gustavo Belzu Ríos

Proyecto desarrollado para la asignatura de Compiladores.
Repositorio:
https://github.com/blackjackbelzu/Proyecto-Interprete
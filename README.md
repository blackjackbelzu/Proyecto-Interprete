# Proyecto Intérprete

Proyecto desarrollado para la materia de Compiladores.

Este proyecto implementa un intérprete para un lenguaje de Alchemist, incluyendo:

- Analizador Léxico
- Analizador Sintáctico 
- Analizador Semántico
- Manejo de errores 

## Estructura del proyecto

```
Proyecto-Interprete/
│
├── azlexico.py          # Analizador léxico
├── sintactico.py        # Analizador sintáctico
├── cod2.txt             # Código fuente de prueba
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.13.7

Verificar la instalación:

```bash
python --version
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/blackjackbelzu/Proyecto-Interprete.git
```

### 2. Entrar al proyecto

```bash
cd Proyecto-Interprete
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecución

Editar el archivo

```
cod2.txt
```

con el programa que se desea analizar.

Luego ejecutar

```bash
python azsintactico.py
```

El programa ejecutará automáticamente:

1. Analizador Léxico
2. Analizador Sintáctico

Mostrando los tokens generados y el resultado del análisis.

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
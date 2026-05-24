# Validador de Códigos con Expresiones Regulares

Proyecto realizado para el reto de la Semana 6 de la materia **Programación para Ciencia de Datos** del Instituto Politécnico Nacional.

## Descripción

Este programa valida diferentes tipos de códigos utilizando expresiones regulares en Python.

Los tipos de códigos soportados son:

- Productos
- Envíos
- Empleados
- Facturas

El programa lee códigos desde la entrada estándar (`stdin`) y genera una salida en formato CSV (`stdout`).

---

# Tecnologías utilizadas

- Python 3
- Expresiones regulares (`re`)
- Entrada estándar (`sys.stdin`)

---

# Estructura del proyecto

```bash
reto-semana-06/
│
├── main.py
├── README.md
├── .gitignore
└── tests/
    ├── codigos.txt
    └── salida_esperada.txt
```

---

# Formatos soportados

## Producto

Formato:

```text
ABC-1234-MX
```

Ejemplo válido:

```text
TEC-0001-MX
```

---

## Envío

Formato:

```text
ENV-YYYY-MM-DD-NNNNNN
```

Ejemplo válido:

```text
ENV-2024-03-15-001234
```

---

## Empleado

Formato:

```text
EMP-XXX-NNNN
```

Ejemplo válido:

```text
EMP-VEN-1234
```

---

## Factura

Formato:

```text
FAC-S-NNNNNN
```

Ejemplo válido:

```text
FAC-A-123456
```

---

# Cómo ejecutar el programa

## Linux / Mac

```bash
python main.py < codigos.txt
```

## Windows PowerShell

```powershell
Get-Content codigos.txt | python main.py
```

## Windows CMD

```cmd
type codigos.txt | python main.py
```

---

# Ejemplo de entrada

```text
TEC-0001-MX
tec-0001-MX
ENV-2024-03-15-001234
EMP-VEN-0123
FAC-A-123456
```

---

# Ejemplo de salida

```csv
codigo,tipo,valido
TEC-0001-MX,producto,VALIDO
tec-0001-MX,producto,INVALIDO
ENV-2024-03-15-001234,envio,VALIDO
EMP-VEN-0123,empleado,INVALIDO
FAC-A-123456,factura,VALIDO
```

---

# Características del programa

- Uso de expresiones regulares
- Validación estricta de formatos
- Validación de rangos de fechas
- Detección automática del tipo de código
- Ignora líneas vacías
- Salida exacta en formato CSV

---

## Autor

**Valery Cruz Salinas**  
Programación para Ciencia de Datos — IPN  
Semestre Febrero-Julio 2026
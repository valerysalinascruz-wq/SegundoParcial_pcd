import sys
import re

DEPA_VALIDOS = ['VEN', 'ADM', 'TEC', 'LOG', 'RHH']
SERIES_VALIDAS = ['A', 'B', 'C', 'D', 'E']


def detectar_tipo(codigo):
    """Detecta el tipo de codigo por su estructura general."""
    if re.match(r'^[A-Za-z]{3}-\d{4}-[A-Za-z]{2}$', codigo):
        return "producto"
    elif re.match(r'^ENV-\d{4}-\d{2}-\d{2}-\d{6}$', codigo):
        return "envio"
    elif re.match(r'^EMP-[A-Za-z]{3}-\d{4}$', codigo):
        return "empleado"
    elif re.match(r'^FAC-[A-Za-z]-\d{6}$', codigo):
        return "factura"
    else:
        return "desconocido"


def validar_producto(codigo):
    """Valida que categoria y pais sean mayusculas."""
    patron = r'^([A-Z]{3})-(\d{4})-([A-Z]{2})$'
    return bool(re.match(patron, codigo))


def validar_envio(codigo):
    """Valida año 2020-2030, mes 01-12, dia 01-31."""
    patron = r'^ENV-(\d{4})-(\d{2})-(\d{2})-(\d{6})$'
    match = re.match(patron, codigo)
    if match:
        anio = int(match.group(1))
        mes = int(match.group(2))
        dia = int(match.group(3))
        return 2020 <= anio <= 2030 and 1 <= mes <= 12 and 1 <= dia <= 31
    return False


def validar_empleado(codigo):
    """Valida departamento valido y numero no empieza con 0."""
    patron = r'^EMP-([A-Z]{3})-(\d{4})$'
    match = re.match(patron, codigo)
    if match:
        dept = match.group(1)
        num = match.group(2)
        return dept in DEPA_VALIDOS and not num.startswith('0')
    return False


def validar_factura(codigo):
    """Valida serie A-E en mayuscula."""
    patron = r'^FAC-([A-Z])-(\d{6})$'
    match = re.match(patron, codigo)
    if match:
        serie = match.group(1)
        return serie in SERIES_VALIDAS
    return False


def validar_codigo(codigo):
    """Detecta tipo y valida. Retorna (tipo, es_valido)."""
    tipo = detectar_tipo(codigo)
    if tipo == "producto":
        return tipo, validar_producto(codigo)
    elif tipo == "envio":
        return tipo, validar_envio(codigo)
    elif tipo == "empleado":
        return tipo, validar_empleado(codigo)
    elif tipo == "factura":
        return tipo, validar_factura(codigo)
    else:
        return "desconocido", False


def main():
    print("codigo,tipo,valido")
    for linea in sys.stdin:
        codigo = linea.strip()
        if not codigo:
            continue
        tipo, es_valido = validar_codigo(codigo)
        print(f"{codigo},{tipo},{'VALIDO' if es_valido else 'INVALIDO'}")


if __name__ == "__main__":
    main()
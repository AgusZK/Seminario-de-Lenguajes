import csv

def extraer_periodo_desde_txt(content_bytes):
    decoded = content_bytes.decode("utf-8").splitlines()
    lector = csv.DictReader(decoded, delimiter=";")
    for fila in lector:
        fila = {key.strip(): value.strip() for key, value in fila.items()}
        if fila.get("ANO4", "").isdigit() and fila.get("TRIMESTRE", "").isdigit():
            return int(fila["ANO4"]), int(fila["TRIMESTRE"])
    return None, None

def ya_esta_registrado(anio, trimestre, dataset_path):
    if not dataset_path.exists():
        return False
    with open(dataset_path, encoding="utf-8") as f:
        lector = csv.DictReader(f, delimiter=';') 
        for fila in lector:
            if int(fila["ANO4"]) == anio and int(fila["TRIMESTRE"]) == trimestre:
                return True
    return False

def verificar_pares_archivos(hogares_path, individuos_path):
    inconsistencias = []

    archivos_hogares = {f.name for f in hogares_path.glob("*.txt")}
    archivos_individuos = {f.name for f in individuos_path.glob("*.txt")}

    def extraer_anio_trimestre(nombre):
        partes = nombre.strip().split("_T")
        if len(partes) != 2:
            return None
        try:
            cod = partes[1].split(".")[0]
            if len(cod) == 3 and cod.isdigit():
                trimestre = int(cod[0])
                anio = 2000 + int(cod[1:])
                return anio, trimestre
        except Exception:
            return None

    claves_hogares = {extraer_anio_trimestre(nombre) for nombre in archivos_hogares}
    claves_individuos = {extraer_anio_trimestre(nombre) for nombre in archivos_individuos}

    claves_hogares.discard(None)
    claves_individuos.discard(None)

    todos_los_periodos = claves_hogares.union(claves_individuos)

    for anio, trimestre in todos_los_periodos:
        if (anio, trimestre) not in claves_hogares:
            inconsistencias.append((anio, trimestre, "hogares"))
        if (anio, trimestre) not in claves_individuos:
            inconsistencias.append((anio, trimestre, "individuos"))

    return inconsistencias

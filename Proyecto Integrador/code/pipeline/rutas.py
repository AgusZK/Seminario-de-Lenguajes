from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent
INDIVIDUOS_PATH = PROJECT_PATH / "data" / "individuos"
HOGARES_PATH = PROJECT_PATH / "data" / "hogares"
PROCESADOS_PATH = PROJECT_PATH / "data" / "procesados"
AGLOMERADOS_COORDENADAS = PROJECT_PATH / "data" / "archivos_auxiliares" / "aglomerados_coordenadas.json"
VALORES_CANASTA = PROJECT_PATH / "data" / "archivos_auxiliares" / "valores-canasta-basica-alimentos.csv"
HOGARES_PROCESADOS_PATH = PROCESADOS_PATH / "hogares.csv"

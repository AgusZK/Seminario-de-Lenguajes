import pandas as pd

# Trimestres como meses
TRIMESTRES = {
    1: [1, 2, 3],
    2: [4, 5, 6],
    3: [7, 8, 9],
    4: [10, 11, 12]
}

def cargar_datos(hogares_path, canasta_path):
    """Carga archivos CSV de hogares y canasta básica y retorna dos DataFrames.

    Args:
        hogares_path (str or Path): Ruta al archivo de hogares.
        canasta_path (str or Path): Ruta al archivo de canasta.

    Returns:
        tuple: DataFrames de hogares y canasta con columnas año y mes en canasta.
    """
    hogares = pd.read_csv(hogares_path, sep=";", encoding="utf-8")
    canasta = pd.read_csv(canasta_path, sep=",", encoding="utf-8", parse_dates=["indice_tiempo"])
    canasta["AÑO"] = canasta["indice_tiempo"].dt.year
    canasta["MES"] = canasta["indice_tiempo"].dt.month
    return hogares, canasta

def analizar_hogares(hogares_df, canasta_df, año, trimestre):
    """Analiza hogares y calcula estadísticas de pobreza para un año y trimestre dados.

    Args:
        hogares_df (DataFrame): Datos de hogares.
        canasta_df (DataFrame): Datos de canasta básica.
        año (int): Año a analizar.
        trimestre (int): Trimestre a analizar.

    Returns:
        tupla: total hogares, pobres, indigentes, CBT, CBA, DataFrame para gráfico.
    """
    hogares_4 = hogares_df[
        (hogares_df["IX_TOT"] == 4) &
        (hogares_df["ANO4"] == año) &
        (hogares_df["TRIMESTRE"] == trimestre)
    ]

    if hogares_4.empty:
        return None, None, None, None, None, None

    meses = TRIMESTRES[trimestre]
    canasta_trim = canasta_df[
        (canasta_df["AÑO"] == año) &
        (canasta_df["MES"].isin(meses))
    ]

    CBT = canasta_trim["canasta_basica_total"].mean()
    CBA = canasta_trim["canasta_basica_alimentaria"].mean()

    indigentes = (hogares_4["ITF"] < CBA).sum()
    pobres_no_indigentes = ((hogares_4["ITF"] >= CBA) & (hogares_4["ITF"] < CBT)).sum()
    no_pobres = (hogares_4["ITF"] >= CBT).sum()

    total = len(hogares_4)
    pobres = indigentes + pobres_no_indigentes

    datos = {
        "Categoría": ["Indigencia", "Pobreza no indigente", "No pobre"],
        "Cantidad": [indigentes, pobres_no_indigentes, no_pobres]
    }

    df_grafico = pd.DataFrame(datos)

    return total, pobres, indigentes, CBT, CBA, df_grafico


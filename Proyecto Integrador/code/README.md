# 📊 encuestAR

Aplicación para la consulta y visualización estadística de datos provenientes de la **Encuesta Permanente de Hogares (EPH)**.

---

## 🧩 ¿Qué es encuestAR?

`encuestAR` es una herramienta interactiva que permite:

- Visualizar estadísticas clave de la EPH de forma clara e intuitiva.
- Realizar consultas sobre los datos disponibles.
- **Actualizar el dataset** cargando nuevos archivos `.txt`

Todo esto desde una interfaz web simple y rápida, construida con **Streamlit**.

---

## 🛠️ Tecnologías utilizadas

- 🐍 **Python**  
- 📦 Módulos nativos de Python (`csv`, `os`, `pathlib`)
- 🌐 **[Streamlit](https://streamlit.io/)** para la interfaz web
- 🧪 **GitLab** para control de versiones y trabajo colaborativo

---

## 🚀 ¿Cómo ejecutar la app?

1. Crea un nuevo directorio y accede al mismo:
   ```bash
   mkdir encuestaApp
   cd encuestaApp

2. (Opcional pero recomendable) Crea un entorno virtual:
   ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows, usa: venv\Scripts\activate


3. Cloná el repositorio y accede a la carpeta code:
   ```bash
   git clone https://gitlab.catedras.linti.unlp.edu.ar/python-2025/proyectos/grupo25/code.git
   cd code
   

3. Instalá las dependencias y corre la app:
   ```bash
   pip install -r requirements.txt
   streamlit run app/inicio.py

---

## 📂 ¿Cómo actualizar los datos?

1. Dirigite a la sección de carga de archivos dentro de la app.
2. Carga dos archivos `.txt` con datos actualizados de la EPH.
3. La app procesará actualizará automáticamente la base de datos.

---

> ⚠️ **Importante:**  
> - La aplicación **no implementa un mecanismo automático para evitar duplicados**.  
> Si se cargan archivos que ya fueron incorporados anteriormente (por ejemplo, un mismo trimestre), la información se agregará nuevamente, generando duplicación de datos.  
> - Aunque se restringe la carga de archivos que no sean `.txt`, el sistema asume que el usuario cargará archivos **adecuados y correspondientes a cada categoría** (por ejemplo, individuos y hogares).  
> Si se cargan archivos incorrectos o mal estructurados, pueden producirse errores o resultados inesperados.



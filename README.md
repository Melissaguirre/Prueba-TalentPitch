# Data Analyst Challenge - TalentPitch

## Descripción
Esta solución procesa datos provenientes de archivos CSV alojados en prueba-talentpitch/data para generar métricas clave sobre los *Flows* (convocatorias), *Resumes* en video y usuarios en TalentPitch, además de otros procesos. El sistema automatiza el análisis, genera reportes (PDF y CSV) e indica insights finales.

La solución está desarrollada en **Python 3.10**, para facilitar mantenibilidad, y ejecución a nivel de compatibilidad de versionamiento.


## Problema Resuelto
Se crea un proceso automatizado para:
- Ingesta, validación y limpieza de datos.
- Cálculo de métricas por Flow.
- Generación de reportes PDF y CSV.
- Envío de reportes por correo.

## Características Principales
- Ingesta y lectura de archivos CSV desde /data
- Validaciones automáticas: IDs, campos requeridos, FK, emails únicos.
- Cálculo de métricas por flow: Participantes únicos, total aplicaciones, votos, visualizaciones, top skills, tasa de conversión, métricas por período (mensual-semanal).
- Generación de reportes consolidados en CSV y PDF.
- Persistencia de datos limpios en SQLite para análisis posteriores.

## Tecnologías Utilizadas
- Python 3.10+
- Pandas
- SQLite
- SQLAlchemy
- FPDF
- SendGrid
- Pydantic

## Prerequisitos
- Python 3.10+
- Pip
- pipenv

Variables de entorno
- SENDGRID_API_KEY
- TEMPLATE_ID
- EMAIL_SENDER
- EMAIL_RECEIVER

## Instalación
Sigue estos pasos para preparar el entorno y ejecutar el proyecto localmente.

1. Clona el repositorio y ve al directorio del proyecto:

```bash
git clone <repo-url>
cd Prueba-TalentPitch
```

2. Opción recomendada con Pipenv:

```bash
# instalar pipenv si no lo tienes
pip install --user pipenv

# instalar dependencias (incluye dev) y abrir shell
pipenv install --dev
pipenv shell
```

3. Alternativa venv + pip:

```bash
# crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# si no existe, puedes crear requirements desde Pipfile con:
# pipenv lock -r > requirements.txt
# e instalar:
pip install -r requirements.txt
```

4. Configura variables de entorno:

```bash
export SENDGRID_API_KEY="<sendgrid-key>"
export TEMPLATE_ID="<template-id>"
export EMAIL_SENDER="sender@example.com"
export EMAIL_RECEIVER="receiver@example.com"
```

## Uso
```bash
# si usas pipenv
pipenv run python src/main.py

# si usas venv
python src/main.py
```

## Estructura del Proyecto

```
Prueba-TalentPitch/
├── Pipfile                    # Dependencias y versiones del proyecto (pipenv)
├── README.md                  
│
├── data/                      # 📁 Archivos CSV de entrada (datos sin procesar)
│   ├── flows.csv              # Convocatorias / Flows
│   ├── users.csv              # Información de usuarios
│   ├── resumes.csv            # Resumes en video de usuarios
│   ├── resumes_exhibited.csv  # Exhibiciones de resumes en flows
│   ├── votes.csv              # Votos recibidos en flows/resumes
│   ├── shares.csv             # Comparticiones de flows
│   ├── views.csv              # Visualizaciones de flows/resumes
│   └── profiles.csv           # Perfiles adicionales de usuarios
│
└── src/                       # 📁 Código fuente del pipeline
    ├── main.py                # Orquestador principal del pipeline
    │
    ├── ingestion/             # 📁 Módulo de ingesta de datos
    │   └── loader.py          # Lectura de CSVs, carga inicial y validación
    │
    ├── processing/            # 📁 Módulo de procesamiento y cálculo de métricas
    │   └── metrics.py         # Funciones para calcular KPIs por Flow
    │                           # (participantes, aplicaciones, votos, skills, etc.)
    │
    ├── reporting/             # 📁 Módulo de generación de reportes
    │   ├── reports.py          # Genera métricas en formato CSV y PDF, al terminar de generarlos, realiza el envío de correo con ambos formatos.
    │
    ├── db/                    # 📁 Módulo de persistencia en base de datos
    │   ├── database.py        # Configuración SQLAlchemy, engine SQLite
    │   ├── models.py          # Modelos ORM (Flow, User, Resume, etc.)
    │   └── save.py            # Persistencia de DataFrames a tablas SQLite
    │
    └── utils/                 # 📁 Utilidades reutilizables para todo el pipeline
        ├── validators.py      # Funciones de validación (IDs, FK, emails, etc.)
        ├── schemas.py         # Definición de campos esperados y relaciones FK
        ├── sendgrid.py        # Servicio para el envío de correos
        |
        └── logger.py          # Configuración de logging
```

### Archivos Clave Explicados

| Archivo | Propósito |
|---------|-----------|
| `src/main.py` | Punto de entrada; orquesta el flujo: load - validate - save in db - calculate metrics - report |
| `src/ingestion/loader.py` | Lee CSVs de `data/`, valida datos con funciones de `validators.py` |
| `src/processing/metrics.py` | Contiene funciones para calcular KPIs (participantes únicos, votos, top skills, etc.) |
| `src/reporting/reports.py` | Genera métricas en un archivo CSV y en un PDF almacena toda la información incluyendo gráficas, conclusiones, recomendaciones.|
| `src/db/database.py` | Define conexión SQLite, activa FK constraints |
| `src/db/models.py` | Modelos SQLAlchemy para las 8 tablas (flows, users, resumes, etc.) |
| `src/db/save.py` | Transforma fechas, convierte DataFrames a registros, realiza el guardado en las tablas.|
| `src/utils/validators.py` | Valida emails únicos, IDs válidos, FK, campos requeridos |
| `src/utils/schemas.py` | Define campos esperados por tabla y relaciones entre ellas|
| `src/utils/sendgrid.py` | Servicio para envío automático de reportes por correo |


## Decisiones de Diseño

- **Separación por capas modular (ingestion - persistence - processing - reporting)**
  - Cada módulo tiene responsabilidad única y bien definida, facilitando mantenimiento y evolución independiente.

- **Pandas para ETL**
  - Librería poderosa y flexible para limpieza, transformación y agregación de datos CSV sin complejidad innecesaria.

- **SQLite + SQLAlchemy**
  - Base de datos liviana sin servidor, perfecta para desarrollo y datasets pequeños-medianos.
  - ORM permite mapeo transparente entre DataFrames y tablas, eliminando SQL manual.

- **FPDF para reportes PDF**
  - Genera PDF con tablas, gráficas y resumen ejecutivo sin dependencias pesadas.

- **SendGrid para envío de correos**
  - Integración sencilla y confiable para distribuir reportes automáticamente.

- **Pydantic para validación de datos**
  - Garantiza que los datos cumplen esquemas esperados, mejorando robustez.


## Cómo Se Ejecuta la Solución

El pipeline sigue este flujo paso a paso:

1. **Carga de datos** (`src/ingestion/loader.py`)
   - Lee cada CSV en `data/` según esquema definido en `src/utils/schemas.py`
   - Llama a `complete_validations()` para cada tabla

2. **Validaciones** (`src/utils/validators.py`)
   - Elimina emails duplicados
   - Remueve filas con campos requeridos faltantes
   - Valida IDs (elimina nulos, duplicados, mantiene los más recientes)
   - Valida referencias FK (elimina filas cuyas FK no existen en tablas referenciadas)

3. **Persistencia** (`src/db/save.py`)
   - Convierte tipos de datos (fechas)
   - Hace bulk insert de todos los DataFrames a tablas SQLite
   - Si hay error, rollback automático para mantener integridad


4. **Cálculo de métricas** (`src/processing/metrics.py`)
   - Agrupa datos por Flow para calcular:
     - Participantes únicos, total aplicaciones, votos totales
     - Visualizaciones únicas y totales, compartidos
     - Distribución por género y rango de edad
     - Top skills más comunes
     - Tasa de conversión (participantes / aplicaciones) * 100
     - Métricas por mes y semana

5. **Generación de reportes** (`src/reporting/reports.py`)
   - Genera CSV multi-sección con todas las métricas
   - Crea PDF con tablas, gráficas, resumen ejecutivo y recomendaciones

6. **Envío de correos** (`src/utils/sendgrid.py`)
   - Envía automáticamente CSV y PDF a direcciones configuradas via SENDGRID_API_KEY
   **importante: (Actualmente los correos llegan a spam con mi configuración actual)**

7. **Finalización**
   - Logs informativos en cada paso
   - Archivos finales disponibles: `talentpitch_data_clean.db`

## Resultados Esperados

Tras ejecutar `pipenv run python src/main.py` (o `python src/main.py` con venv), obtendrás:

### Archivos de salida:

2. **`talentpitch_data_clean.db`**
   - Base SQLite con 8 tablas:
     - `flows`, `users`, `resumes`, `resumes_exhibited`
     - `votes`, `shares`, `views`, `profiles`
   - Datos limpios (validados, sin duplicados, con FK intactas)

4. **Correos enviados**
   - CSV y PDF automáticamente distribuidos a `EMAIL_RECEIVER` via SendGrid

### Ejemplo de logs esperados:

```
2025-12-02 10:30:00 - INFO - root - Loading data from CSV files
2025-12-02 10:30:01 - INFO - root - Loading flows
2025-12-02 10:30:01 - INFO - root - Validating unique emails
...
2025-12-02 10:30:05 - INFO - root - Mail sent successfully
2025-12-02 10:30:06 - INFO - root - Data process complete
```

## Testing
[Cómo ejecutar los tests y qué cobertura tienen]
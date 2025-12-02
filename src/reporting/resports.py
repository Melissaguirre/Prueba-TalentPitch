import pandas as pd

from processing.metrics import get_all_metrics_as_dict

from fpdf import FPDF
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import tempfile


class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Reporte de Métricas", 0, 1, "C")
        self.ln(3)

    def add_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1)
        self.ln(2)

    def add_paragraph(self, text):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def add_table(self, df: pd.DataFrame):
        if df.empty:
            self.add_paragraph("No hay datos disponibles.")
            return

        self.set_font("Arial", "B", 9)
        col_width = self.w / (len(df.columns) + 1)
        for col in df.columns:
            self.cell(col_width, 8, str(col), border=1)
        self.ln()
        self.set_font("Arial", "", 9)
        for _, row in df.iterrows():
            for item in row:
                self.cell(col_width, 8, str(item), border=1)
            self.ln()
        self.ln(5)

    def add_figure(self, fig):
        with tempfile.NamedTemporaryFile(suffix=".png") as tmpfile:
            fig.savefig(tmpfile.name, bbox_inches="tight")
            self.image(tmpfile.name, w=170)
            plt.close(fig)
        self.ln(5)


def transform_metrics(dataframes: dict):
    def merge_metrics(df_main: pd.DataFrame, df_metric: pd.DataFrame):
        return df_main.merge(df_metric, on="ID Flow", how="left")

    kpis = dataframes["Participantes Únicos"]
    kpis = merge_metrics(kpis, dataframes["Total Aplicaciones"])
    kpis = merge_metrics(kpis, dataframes["Votos Totales"])
    kpis = merge_metrics(kpis, dataframes["Compartidos"])
    kpis = merge_metrics(kpis, dataframes["Visualizaciones Únicas"])
    kpis = merge_metrics(kpis, dataframes["Visualizaciones Totales"])
    kpis = kpis.fillna(0)
    kpis["ID Flow"] = kpis["ID Flow"].astype(str)

    kpis = kpis.rename(
        columns={
            "Participantes Únicos": "Participantes",
            "Total Aplicaciones": "Aplicaciones",
            "Votos Totales": "Votos",
            "Visualizaciones Únicas": "V. Unicas",
            "Visualizaciones Totales": "V. Totales",
        }
    )

    return kpis


def generate_report_pdf(dataframes: dict, filename="report.pdf", version="1.0"):
    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    pdf.add_paragraph(
        f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    df_dates = dataframes["Métricas por Mes"]
    if not df_dates.empty:
        start_period = df_dates["Mes"].min()
        end_period = df_dates["Mes"].max()
        pdf.add_paragraph(f"Período analizado: {start_period} a {end_period}")
    else:
        pdf.add_paragraph("Período analizado: No disponible")
    pdf.add_paragraph(f"Versión del reporte: {version}")

    pdf.add_title("KPIS")
    kpis = transform_metrics(dataframes)
    pdf.add_table(kpis)

    pdf.add_title("Distribución por Género")
    pdf.add_table(dataframes["Distribución por Género"])
    pdf.add_title("Distribución por Edad")
    pdf.add_table(dataframes["Distribución por Edad"])
    pdf.add_title("Top Skills")
    pdf.add_table(dataframes["Top Skills"])
    pdf.add_title("Tasa de Conversión")
    pdf.add_table(dataframes["Tasa de Conversión"])

    pdf.add_title("Visualizaciones de Tendencias")
    fig_mes, ax_mes = plt.subplots()
    df_mes = dataframes["Métricas por Mes"]
    ax_mes.bar(df_mes["Mes"], df_mes["Total Aplicaciones"], color="#4c72b0")
    ax_mes.set_title("Aplicaciones por Mes")
    ax_mes.set_xlabel("Mes")
    ax_mes.set_ylabel("Total Aplicaciones")
    plt.xticks(rotation=45)
    pdf.add_figure(fig_mes)

    fig_sem, ax_sem = plt.subplots()
    df_sem = dataframes["Métricas por Semana"]
    ax_sem.bar(df_sem["Semana"], df_sem["Total Aplicaciones"], color="#55a868")
    ax_sem.set_title("Aplicaciones por Semana")
    ax_sem.set_xlabel("Semana")
    ax_sem.set_ylabel("Total Aplicaciones")
    plt.xticks(rotation=45)
    pdf.add_figure(fig_sem)

    pdf.add_title("Conclusiones y Recomendaciones")
    pdf.add_title("Conclusiones")
    pdf.add_paragraph(
        "1. Los flows 1 y 3 destacan en votos compartidos, visualizaciones, lo cual demuestra un contenido o temática atractiva para la audiencia."
    )
    pdf.add_paragraph(
        "3. Las participaciones por flow tiene un promedio de (2-3 personas)."
    )
    pdf.add_paragraph(
        "4. El público es bastante equilibrado en género pero en edad se observa una mayor concentración en el rango de 25-34 años, lo que sugiere enfocar estrategias de marketing y contenido para también atraer perfiles de otras edades."
    )
    pdf.add_paragraph(
        "5. Las habilidades perdominantes observadas en los participantes están enfocados a programación, UX y data, lo que permite orientar campañas y flows hacia estas áreas."
    )
    pdf.add_paragraph(
        "6. Se observa una notable caída de actividad en noviembre, (-44% vs octubre), lo cual podría indicar menor promoción, o alcance durante ese mes."
    )
    pdf.add_paragraph(
        "2. La tasa de conversión del 100% indica una excelente experiencia de usuario con los flows ya que el mismo número de participantes es igual las aplicaciones."
    )

    pdf.add_title("Recomendaciones")
    pdf.add_paragraph(
        "1. El promedio de participaciones de flows es bajo, lo cual aborda un mejora prioritaria para aumentar difusión, llegar a más usuarios, hacer los flows más visibles, usar más campañas, mejorar las presentaciones, etc."
    )
    pdf.add_paragraph(
        "2. Explorar contenido específico para audiencias jóvenes, dado que actualmente no participan usuarios menores de 25."
    )
    pdf.add_paragraph(
        "3. Crear flows orientados a habilidades técnicas populares como programación, UX y data para atraer más participantes."
    )

    pdf.output(filename)


def create_csv_report(data: dict[str, pd.DataFrame], filename="metrics_report.csv"):
    """
    Write multiple dataframes to a single CSV file with section headers.

    Each metric is preceded by a header line "-- metric_name --" followed by
    the dataframe content and blank lines for separation.

    Args:
        data: Dictionary mapping metric names to their DataFrames
        filename: Output CSV file path (default: "metrics_report.csv")
    """
    with open("metrics_report.csv", "w", encoding="utf-8") as file:
        for title, df_metric in data.items():
            file.write(f" -- {title} --\n")
            df_metric.to_csv(file, index=False)
            file.write("\n\n")


def save_metrics_csv_pdf(data: dict[str, pd.DataFrame]):
    """
    Compute metrics and generate both CSV and PDF reports.

    Reporting flow:
    1. Compute all metrics from raw data
    2. Save metrics to CSV file
    3. Generate PDF report with formatted tables

    Args:
        data: Dictionary of validated DataFrames from the loading phase
    """
    metrics = get_all_metrics_as_dict(data)

    create_csv_report(metrics, filename="metrics_report.csv")
    generate_report_pdf(metrics, filename="metrics_report.pdf")

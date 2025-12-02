import pandas as pd


def unique_participants(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Count unique participants (users) by Flow.

    Args:
        data: Dictionary containing 'resumes' and 'resumes_exhibited' DataFrames

    Returns:
        DataFrame with columns: 'ID Flow', 'Participantes Únicos'
    """
    resumes_df = data.get("resumes")
    resumes_exhibited_df = data.get("resumes_exhibited")

    joined_df = resumes_exhibited_df.merge(
        resumes_df[["id", "user_id"]], left_on="resume_id", right_on="id", how="left"
    )
    group_participants = (
        joined_df.groupby("model_id")["user_id"].nunique().reset_index()
    )
    unique_participants = group_participants.rename(
        columns={"model_id": "ID Flow", "user_id": "Participantes Únicos"}
    )
    return unique_participants


def application_total(df_resumes_exhibited: pd.DataFrame) -> pd.DataFrame:
    """
    Count total applications (resumes) submitted by Flow.

    Args:
        df_resumes_exhibited: DataFrame containing resume exhibition records

    Returns:
        DataFrame with columns: 'ID Flow', 'Total Aplicaciones'
    """
    group_resumes_exhibited = (
        df_resumes_exhibited.groupby("model_id")["id"].count().reset_index()
    )
    total_applications = group_resumes_exhibited.rename(
        columns={"model_id": "ID Flow", "id": "Total Aplicaciones"}
    )
    return total_applications


def total_votes(df_votes: pd.DataFrame) -> pd.DataFrame:
    """
    Sum total votes received by Flow.

    Args:
        df_votes: DataFrame containing vote records with 'model_id' and 'value' columns

    Returns:
        DataFrame with columns: 'ID Flow', 'Votos Totales'
    """
    group_votes_flow = df_votes.groupby("model_id")["value"].sum().reset_index()
    total_votes_flow = group_votes_flow.rename(
        columns={"model_id": "ID Flow", "value": "Votos Totales"}
    )
    return total_votes_flow


def total_shared(df_shares: pd.DataFrame) -> pd.DataFrame:
    """
    Count total shares by Flow.

    Args:
        df_shares: DataFrame containing share records with 'model_id' column

    Returns:
        DataFrame with columns: 'ID Flow', 'Compartidos'
    """
    group_shares = df_shares.groupby("model_id")["id"].count().reset_index()
    total_shared = group_shares.rename(
        columns={"model_id": "ID Flow", "id": "Compartidos"}
    )
    return total_shared


def unique_views(df_views: pd.DataFrame) -> pd.DataFrame:
    """
    Count unique users who viewed each Flow.

    Args:
        df_views: DataFrame containing view records with 'model_id' and 'user_id' columns

    Returns:
        DataFrame with columns: 'ID Flow', 'Visualizaciones Únicas'
    """
    group_unique_views = df_views.groupby("model_id")["user_id"].nunique().reset_index()
    unique_views = group_unique_views.rename(
        columns={"model_id": "ID Flow", "user_id": "Visualizaciones Únicas"}
    )
    return unique_views


def total_views(df_views: pd.DataFrame) -> pd.DataFrame:
    """
    Count total views by Flow.

    Args:
        df_views: DataFrame containing view records with 'model_id' column

    Returns:
        DataFrame with columns: 'ID Flow', 'Visualizaciones Totales'
    """
    group_total_views = df_views.groupby("model_id")["id"].count().reset_index()
    total_views = group_total_views.rename(
        columns={"model_id": "ID Flow", "id": "Visualizaciones Totales"}
    )
    return total_views


def group_by_gender(user_df: pd.DataFrame):
    """
    Group users by gender to count.

    Args:
        user_df: DataFrame containing user records with 'gender' column

    Returns:
        DataFrame with columns: 'Género', 'Cantidad'
    """
    gender_group = user_df.groupby("gender")["id"].count().reset_index()
    fitered_gender = gender_group.rename(columns={"gender": "Género", "id": "Cantidad"})
    return fitered_gender


def group_by_age(user_df: pd.DataFrame) -> pd.DataFrame:
    """
    Group users by age ranges based on birth_date.

    Age ranges: <18, 18-25, 26-55, 56+

    Args:
        user_df: DataFrame containing user records with 'birth_date' column

    Returns:
        DataFrame with columns: 'Rango Edad', 'Cantidad'
    """
    year_current = pd.Timestamp.now().year
    user_df["birth_date"] = pd.to_datetime(user_df["birth_date"], errors="coerce")
    user_df["age"] = year_current - user_df["birth_date"].dt.year

    young = user_df[user_df["age"].between(0, 17)].shape[0]
    young_adults = user_df[user_df["age"].between(18, 25)].shape[0]
    adults = user_df[user_df["age"].between(26, 55)].shape[0]
    older_adults = user_df[user_df["age"] >= 56].shape[0]
    group_ages = pd.DataFrame(
        {
            "Rango Edad": ["<18", "18-25", "26-55", "56+"],
            "Cantidad": [young, young_adults, adults, older_adults],
        },
    )
    return group_ages


def calculate_conversion_rate(
    participants_df: pd.DataFrame, applications_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate conversion rate as (unique participants / total applications) × 100.

    Args:
        participants_df: DataFrame with 'ID Flow' and 'Participantes Únicos' columns
        applications_df: DataFrame with 'ID Flow' and 'Total Aplicaciones' columns

    Returns:
        Merged DataFrame with 'Tasa Conversión' column (percentage values)
    """
    conversion_df = participants_df.merge(applications_df, on="ID Flow", how="inner")
    conversion_df["Tasa Conversión"] = (
        conversion_df["Participantes Únicos"] / conversion_df["Total Aplicaciones"]
    ) * 100
    return conversion_df


def top_skills(resumes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract the most common skills from resumes.

    Skills are cleaned and converted to lowercase. Handles list format: "['skill1', 'skill2']"

    Args:
        resumes_df: DataFrame containing resume records with 'skills' column

    Returns:
        DataFrame with columns: 'Skill', 'Cantidad' (sorted by count descending)
    """
    skills_clean = (
        resumes_df["skills"]
        .str.replace("[", "")
        .str.replace("]", "")
        .str.replace("'", "")
    )
    skills_list = skills_clean.str.split(",")
    skills_exploded = skills_list.explode()
    skills_exploded = skills_exploded.str.strip().str.lower()

    top_skills = skills_exploded.value_counts().reset_index()
    top_skills.columns = ["Skill", "Cantidad"]
    return top_skills


def metrics_per_month(df_resumes_exhibited: pd.DataFrame) -> pd.DataFrame:
    """
    Add application metrics by month (YYYY-MM format).

    Args:
        df_resumes_exhibited: DataFrame containing resume exhibition records with 'created_at' column

    Returns:
        DataFrame with columns: 'Mes' (YYYY-MM), 'Total Aplicaciones'
    """
    df_metric_month = df_resumes_exhibited.copy()
    df_metric_month["created_at"] = pd.to_datetime(
        df_metric_month["created_at"], errors="coerce"
    )
    df_metric_month["year_month"] = (
        df_metric_month["created_at"].dt.to_period("M").astype(str)
    )
    monthly_metrics = df_metric_month.groupby("year_month")["id"].count().reset_index()
    monthly_metrics.columns = ["Mes", "Total Aplicaciones"]

    return monthly_metrics


def metrics_per_week(df_resumes_exhibited: pd.DataFrame) -> pd.DataFrame:
    """
    Add application metrics by week (YYYY-WNN format).

    Args:
        df_resumes_exhibited: DataFrame containing resume exhibition records with 'created_at' column

    Returns:
        DataFrame with columns: 'Semana' (YYYY-WNN), 'Total Aplicaciones'
    """
    df_metric_week = df_resumes_exhibited.copy()
    df_metric_week["created_at"] = pd.to_datetime(
        df_metric_week["created_at"], errors="coerce"
    )
    df_metric_week["year_week"] = df_metric_week["created_at"].dt.strftime("%Y-W%U")
    weekly_metrics = df_metric_week.groupby("year_week")["id"].count().reset_index()
    weekly_metrics.columns = ["Semana", "Total Aplicaciones"]

    return weekly_metrics


def get_all_metrics_as_dict(data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:  
    """
    Compute all available metrics:
    - Participantes Únicos
    - Total Aplicaciones
    - Votos Totales
    - Compartidos
    - Visualizaciones Únicas
    - Visualizaciones Totales
    - Distribución por Género
    - Distribución por Edad
    - Tasa de Conversión
    - Top Skills
    - Métricas por Mes
    - Métricas por Semana

    Args:
        data: Dictionary containing DataFrames by table name:
              'resumes', 'resumes_exhibited', 'votes', 'shares', 'views', 'users'

    Returns:
        Dictionary mapping metric names to their respective DataFrames
    """
    metrics = {}

    metrics["Participantes Únicos"] = unique_participants(data)
    metrics["Total Aplicaciones"] = application_total(data["resumes_exhibited"])
    metrics["Votos Totales"] = total_votes(data["votes"])
    metrics["Compartidos"] = total_shared(data["shares"])
    metrics["Visualizaciones Únicas"] = unique_views(data["views"])
    metrics["Visualizaciones Totales"] = total_views(data["views"])
    metrics["Distribución por Género"] = group_by_gender(data["users"])
    metrics["Distribución por Edad"] = group_by_age(data["users"])

    metrics["Tasa de Conversión"] = calculate_conversion_rate(
        metrics["Participantes Únicos"],
        metrics["Total Aplicaciones"]
    )

    metrics["Top Skills"] = top_skills(data["resumes"])
    metrics["Métricas por Mes"] = metrics_per_month(data["resumes_exhibited"])
    metrics["Métricas por Semana"] = metrics_per_week(data["resumes_exhibited"])

    return metrics



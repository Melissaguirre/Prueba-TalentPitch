"""
Test SIMPLE para métricas - entender cómo testear cálculos.

Este archivo muestra:
1. Cómo crear datos de prueba realistas
2. Cómo probar funciones matemáticas/agregaciones
3. Cómo verificar que los cálculos sean correctos
"""

import pandas as pd
from processing.metrics import (
    unique_participants,
    application_total,
    total_votes,
    total_shared,
    unique_views,
    total_views,
    group_by_gender,
    group_by_age,
    calculate_conversion_rate,
    top_skills,
    metrics_per_month,
    metrics_per_week,
)


def test_unique_participants():
    df_resumes = pd.DataFrame(
        data={
            "id": [
                1,
                3,
                7,
                2,
                5,
                8,
                10,
                4,
            ],
            "user_id": [
                1,
                3,
                7,
                2,
                5,
                8,
                10,
                4,
            ],
        }
    )
    df_resumes_exhibited = pd.DataFrame(
        data={
            "id": [
                1,
                6,
                11,
                12,
                15,
                18,
                2,
                7,
            ],
            "resume_id": [1, 3, 7, 2, 5, 8, 10, 4],
            "model_id": [1, 1, 1, 2, 2, 2, 3, 3],
        }
    )
    result_mock = pd.DataFrame(
        data={"ID Flow": [1, 2, 3], "Participantes Únicos": [3, 3, 2]}
    )
    data = {"resumes": df_resumes, "resumes_exhibited": df_resumes_exhibited}
    result = unique_participants(data)
    assert result.equals(result_mock)


def test_application_total():
    df_resumes_exhibited = pd.DataFrame(
        data={
            "id": [
                1,
                6,
                11,
                12,
            ],
            "resume_id": [1, 3, 7, 2],
            "model_id": [1, 2, 1, 3],
        }
    )
    result_mock = pd.DataFrame(data={"ID Flow": [1, 2, 3], "Total Aplicaciones": [2, 1, 1]})
    print(result_mock)
    result = application_total(df_resumes_exhibited)
    print(result)
    assert result.equals(result_mock)


def test_total_votes():
    df_votes = pd.DataFrame(
        data={
            "id": [
                1,
                6,
                11,
                12,
            ],
            "value": [4.5, 4.8, 4.2, 4.2],
            "model_id": [1, 2, 1, 3],
        }
    )
    result_mock = pd.DataFrame(
        data={"ID Flow": [1, 2, 3], "Votos Totales": [8.7, 4.8, 4.2]}
    )
    result = total_votes(df_votes)
    assert result.equals(result_mock)


def test_total_shares():
    df_shares = pd.DataFrame(
        data={
            "id": [
                1,
                2,
                3,
                5,
                7,
                12,
            ],
            "model_id": [1, 2, 1, 3, 3, 1],
        }
    )
    result_mock = pd.DataFrame(data={"ID Flow": [1, 2, 3], "Compartidos": [3, 1, 2]})
    result = total_shared(df_shares)
    assert result.equals(result_mock)


def test_unique_views():
    df_unique_views = pd.DataFrame(
        data={
            "id": [
                1,
                2,
                3,
                5,
                7,
                12,
            ],
            "model_id": [1, 2, 1, 3, 3, 1],
            "user_id": [
                1,
                3,
                1,
                2,
                4,
                8,
            ],
        }
    )
    result_mock = pd.DataFrame(
        data={"ID Flow": [1, 2, 3], "Visualizaciones Únicas": [2, 1, 2]}
    )
    result = unique_views(df_unique_views)
    assert result.equals(result_mock)


def test_total_views():
    df_total_views = pd.DataFrame(
        data={
            "id": [
                1,
                2,
                3,
                5,
                7,
                12,
            ],
            "model_id": [1, 2, 1, 3, 3, 1],
            "user_id": [
                1,
                3,
                1,
                2,
                4,
                8,
            ],
        }
    )
    result_mock = pd.DataFrame(
        data={"ID Flow": [1, 2, 3], "Visualizaciones Totales": [3, 1, 2]}
    )
    result = total_views(df_total_views)
    assert result.equals(result_mock)


def test_group_gender():
    df_gender = pd.DataFrame(
        data={
            "id": [
                1,
                2,
                3,
                5,
                7,
                12,
            ],
            "gender": ["M", "F", "M", "M", "F", "M"],
        }
    )
    result_mock = pd.DataFrame(data={"Género": ["F", "M"], "Cantidad": [2, 4]})
    result = group_by_gender(df_gender)
    assert result.equals(result_mock)


def test_group_gender():
    df_age = pd.DataFrame(
        data={
            "birth_date": [
                pd.Timestamp("1990-05-15"),
                pd.Timestamp("1992-12-11"),
                pd.Timestamp("1990-06-06"),
                pd.Timestamp("1992-07-22"),
                pd.Timestamp("1993-02-14"),
            ],
        }
    )
    result_mock = pd.DataFrame(
        data={"Rango Edad": ["<18", "18-25", "26-55", "56+"], "Cantidad": [0, 0, 5, 0]}
    )
    result = group_by_age(df_age)
    assert result.equals(result_mock)


def test_calculate_conversion_rate():
    df_resumes = pd.DataFrame(
        data={
            "id": [
                1,
                3,
                7,
                2,
                5,
                8,
                10,
                4,
            ],
            "user_id": [
                1,
                3,
                7,
                2,
                5,
                8,
                10,
                4,
            ],
        }
    )
    df_resumes_exhibited = pd.DataFrame(
        data={
            "id": [
                1,
                6,
                11,
                12,
                15,
                18,
                2,
                7,
            ],
            "resume_id": [1, 3, 7, 2, 5, 8, 10, 4],
            "model_id": [1, 1, 1, 2, 2, 2, 3, 3],
        }
    )
    df_participants = unique_participants(
        {"resumes": df_resumes, "resumes_exhibited": df_resumes_exhibited}
    )
    df_applications = application_total(df_resumes_exhibited)
    result_mock = pd.DataFrame(
        data={
            "ID Flow": [1, 2, 3],
            "Participantes Únicos": [3, 3, 2],
            "Total Aplicaciones": [3, 3, 2],
            "Tasa Conversión": [100.0, 100.0, 100.0],
        }
    )
    result = calculate_conversion_rate(df_participants, df_applications)
    assert result.equals(result_mock)
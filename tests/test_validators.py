"""
Test SIMPLE para entender cómo funcionan los tests.

Este archivo muestra:
1. Cómo importar funciones del proyecto
2. Cómo crear datos de prueba con Pandas
3. Cómo verificar que una función hace lo correcto
4. Cómo ejecutar: pytest tests/test_validators_simple.py -v
"""

import pandas as pd
from utils.validators import (
    validation_emails_uniques,
    validation_required_fields,
    validation_valid_ids,
    validation_foreign_keys,
)


def test_validation_emails_uniques():
    df_user = pd.DataFrame(
        data={
            "id": [1, 2, 3, 4],
            "email": [
                "test@gmail.com",
                "ana@gmail.com",
                "juan@gmail.com",
                "test@gmail.com",
            ],
        }
    )
    result_mock = df_user.drop_duplicates(subset=["email"])
    result = validation_emails_uniques(df_user)
    assert result.equals(result_mock)


def test_no_remove_email():
    df_user = pd.DataFrame(
        data={
            "id": [1, 2, 3, 4],
        }
    )
    result = validation_emails_uniques(df_user)
    assert result.equals(df_user)


def test_validation_required_fields_delete_null():
    df_resumes = pd.DataFrame(
        data={
            "id": [1, 2, 3, 4],
            "user_id": [1, 3, None, 6],
            "name": [
                "Desarrollador Python Senior",
                "Cloud Architect",
                "Data Analyst BI",
                None,
            ],
            "created_at": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"],
        }
    )

    required_fields = ["id", "user_id", "name"]
    result_mock = df_resumes.dropna(subset=required_fields)
    result = validation_required_fields(df_resumes, required_fields)
    assert result.equals(result_mock)


def test_validation_required_fields_without_nulos():
    df_resumes = pd.DataFrame(
        data={
            "id": [1, 2, 3],
            "user_id": [1, 3, 4],
            "name": [
                "Desarrollador Python Senior",
                "Cloud Architect",
                "Data Analyst BI",
            ],
            "created_at": ["2025-01-01", "2025-01-02", "2025-01-03"],
        }
    )

    required_fields = ["id", "user_id", "name"]
    result = validation_required_fields(df_resumes, required_fields)
    assert result.equals(df_resumes)


def test_validation_valid_ids():
    df_resumes = pd.DataFrame(
        data={
            "id": [1, 1, 2, None],
            "user_id": [1, 5, 8, 7],
            "name": [
                "Desarrollador Python Senior",
                "Cloud Architect",
                "Data Analyst BI",
                "UX Researcher",
            ],
            "created_at": [
                "2025-01-01",
                "2025-01-02",
                "2025-01-03",
                "2025-01-04",
            ],
        }
    )
    result_mock = pd.DataFrame(
        data={
            "id": [1, 2],
            "user_id": [5, 8],
            "name": [
                "Cloud Architect",
                "Data Analyst BI",
            ],
            "created_at": ["2025-01-02", "2025-01-03"],
        }
    )
    result = validation_valid_ids(df_resumes, "test_resumes")
    result_mock.index = result.index
    assert result.equals(result_mock)


def test_validation_foreign_keys():
    df_resumes = pd.DataFrame(
        data={
            "id": [1, 2, 3, 4],
            "user_id": [1, 5, 20, 9],
            "name": [
                "Desarrollador Python Senior",
                "Cloud Architect",
                "Data Analyst BI",
                "UX Researcher",
            ],
        }
    )

    df_users = pd.DataFrame(
        data={
            "id": [1, 2, 9],
            "name": ["Juan Pérez", "María García", "Ana Martínez"],
        }
    )
    result_mock = pd.DataFrame(
        data={
            "id": [1, 4],
            "user_id": [1, 9],
            "name": ["Desarrollador Python Senior", "UX Researcher"],
        }
    )

    data = {"resumes": df_resumes, "users": df_users}
    result = validation_foreign_keys(df_resumes, "resumes", data)
    result_mock.index = result.index
    assert result.equals(result_mock)


def test_validation_foreign_keys_without_fk():
    df_users = pd.DataFrame(
        data={
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "email": ["alice@test.com", "bob@test.com", "charlie@test.com"],
        }
    )

    data = {"users": df_users}
    result = validation_foreign_keys(df_users, "users", data)
    assert result.equals(df_users)

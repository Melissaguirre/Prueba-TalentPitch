from db.models import Flow, User, Resume, ResumeExhibited, Vote, View, Profile

FIELDS_FILES = {
    "flows": ["id", "name", "slug", "description", "status", "created_at", "views"],
    "users": [
        "id",
        "name",
        "email",
        "slug",
        "phone",
        "country",
        "city",
        "gender",
        "birth_date",
        "created_at",
    ],
    "resumes": [
        "id",
        "user_id",
        "name",
        "slug",
        "video",
        "views",
        "level_experience",
        "status",
        "role_name",
        "skills",
        "created_at",
    ],
    "resumes_exhibited": [
        "id",
        "resume_id",
        "model_id",
        "model_type",
        "sent_at",
        "created_at",
    ],
    "votes": ["id", "model_id", "model_type", "user_id", "value", "created_at"],
    "shares": ["id", "model_id", "model_type", "user_id", "created_at"],
    "views": ["id", "model_id", "model_type", "user_id", "type", "created_at"],
    "profiles": [
        "user_id",
        "skills",
        "tools",
        "languages",
        "dream_brands",
        "dream_roles",
        "areas_of_interest",
    ],
}

FIELDS_FK = {
    "resumes": {"user_id": "users"},
    "resumes_exhibited": {
        "resume_id": "resumes",
        "model_id": "flows",
    },
    "votes": {
        "model_id": "flows",
        "user_id": "users",
    },
    "shares": {
        "model_id": "flows",
        "user_id": "users",
    },
    "views": {
        "model_id": "flows",
        "user_id": "users",
    },
    "profiles": {"user_id": "users"},
}

TABLES_MAP = {
    "flows": Flow,
    "users": User,
    "resumes": Resume,
    "resumes_exhibited": ResumeExhibited,
    "votes": Vote,
    "views": View,
    "profiles": Profile,
}

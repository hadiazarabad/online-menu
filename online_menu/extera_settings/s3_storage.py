from decouple import config

MINIO_ENDPOINT = config("MINIO_ENDPOINT_URL")
MINIO_BUCKET   = config("MINIO_BUCKET_NAME")
MINIO_KEY      = config("MINIO_ACCESS_KEY")
MINIO_SECRET   = config("MINIO_SECRET_KEY")
REGION_NAME = config("REGION_NAME")

COMMON_S3_OPTIONS = {
    "access_key": MINIO_KEY,
    "secret_key": MINIO_SECRET,
    "bucket_name": MINIO_BUCKET,
    "endpoint_url": MINIO_ENDPOINT,      # important for MinIO / S3-compatible endpoints :contentReference[oaicite:2]{index=2}
    "region_name": REGION_NAME,          # set when using endpoint_url to avoid auth/query errors :contentReference[oaicite:3]{index=3}
    "addressing_style": "path",          # often needed with IP/custom endpoints :contentReference[oaicite:4]{index=4}
    "signature_version": "s3v4",
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            **COMMON_S3_OPTIONS,
            "location": "media",
            "file_overwrite": False,
        },
    },

    # Static files (collectstatic)
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            **COMMON_S3_OPTIONS,
            "location": "static",
            "querystring_auth": False,
            "object_parameters": {
                "CacheControl": "max-age=31536000, immutable",
            },
        },
    },
}
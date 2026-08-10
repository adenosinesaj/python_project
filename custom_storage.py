from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class SupabaseMediaStorage(S3Boto3Storage):
    location = ''
    file_overwrite = False

    def url(self, name):
        # Generates clean, public Supabase URLs: https://<project>.supabase.co/storage/v1/object/public/media/<file>
        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{settings.AWS_STORAGE_BUCKET_NAME}/{name}"
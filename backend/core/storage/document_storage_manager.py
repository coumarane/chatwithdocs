import boto3
import mimetypes
from io import BytesIO
from fastapi import UploadFile, HTTPException
from core.config.config import settings


class DocumentStorageManager:
    """Handles document storage in MinIO using boto3."""

    # Allowed File Types & Max File Size (10MB)
    ALLOWED_FILE_TYPES = {"pdf", "docx", "txt"}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    def __init__(self):
        """Initialize the MinIO client using boto3."""
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=f"{settings.MINIO_ENDPOINT}",
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY
        )
        self.bucket_name = settings.MINIO_BUCKET

        # Ensure bucket exists
        if not self.bucket_exists(self.bucket_name):
            self.create_bucket(self.bucket_name)

    def create_bucket(self, bucket_name: str):
        """Create MinIO bucket if it does not exist."""
        try:
            self.s3_client.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        except Exception as e:
            print(f"Error creating bucket: {e}")

    def bucket_exists(self, bucket_name: str) -> bool:
        """Check if MinIO bucket exists."""
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except Exception:
            return False

    async def validate_file(self, file: UploadFile):
        """Validates file format and size."""

        # Extract File Metadata
        file_name = file.filename
        file_type = file.content_type or mimetypes.guess_type(file.filename)[0] or "application/octet-stream"
        file_extension = file.filename.split(".")[-1].lower()
        file_size = len(await file.read())  # Get file size

        if file_extension not in self.ALLOWED_FILE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid file format. Allowed: PDF, DOCX, TXT.")
        if file_size > self.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size exceeds the 10MB limit.")

        # Reset file stream after reading size
        await file.seek(0)

    async def store_file(self, file: UploadFile, user_id: str) -> str:
        """Uploads the file to MinIO and returns the file URL."""
        await self.validate_file(file)

        file_data = await file.read()
        file_stream = BytesIO(file_data)
        file_stream.seek(0)  # Reset file position before upload

        # Store files in per-user directories
        file_path = f"user_{user_id}/{file.filename}"
        content_type = file.content_type or mimetypes.guess_type(file.filename)[0] or "application/octet-stream"

        try:
            self.s3_client.upload_fileobj(
                Fileobj=file_stream,
                Bucket=self.bucket_name,
                Key=file_path,
                ExtraArgs={"ContentType": content_type}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

        # Return file URL
        return f"{settings.MINIO_ENDPOINT}/{self.bucket_name}/{file_path}"

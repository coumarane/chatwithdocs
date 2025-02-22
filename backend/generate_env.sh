#!/bin/bash

# Generate random credentials for MinIO
MINIO_ACCESS_KEY=$(openssl rand -hex 16)
MINIO_SECRET_KEY=$(openssl rand -hex 32)

# Write values to .env.dev
cat <<EOF > .env.dev
# MinIO Environment Variables
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY
MINIO_SECRET_KEY=$MINIO_SECRET_KEY
MINIO_BUCKET=chatdoc-bucket
EOF

echo "Generated .env.dev with MinIO credentials:"
cat .env.dev

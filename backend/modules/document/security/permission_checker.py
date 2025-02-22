from fastapi import HTTPException, status


class PermissionChecker:
    """Centralized permission logic for user actions."""

    @staticmethod
    def check_document_upload_permission(user):
        """Check if the user can upload documents for the given organization."""
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        # if organization_id not in user.organizations:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="User does not have permission to upload documents for this organization"
        #     )

        if user.upload_quota <= 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Upload quota exceeded"
            )

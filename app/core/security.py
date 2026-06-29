from fastapi import HTTPException, status


def get_current_user_placeholder() -> None:
    """Authentication placeholder for future implementation."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication layer is not implemented yet.",
    )

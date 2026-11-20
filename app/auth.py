import os
import os

from dotenv import load_dotenv
from fastapi import Header, HTTPException, status

load_dotenv()

ALLOWED_CODES = {
    code.strip()
    for code in os.getenv("INVITE_CODES", "").split(",")
    if code.strip()
}


def verify_invite_code(
    x_invite_code: str | None = Header(default=None),
) -> str:
    if not ALLOWED_CODES:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="رموز الدعوة غير مهيأة على الخادم",
        )

    if not x_invite_code or x_invite_code.strip() not in ALLOWED_CODES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="رمز الدعوة غير صحيح أو مفقود",
        )

    return x_invite_code.strip()

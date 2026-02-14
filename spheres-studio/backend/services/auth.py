"""
SPHERES Studio — Authentication Service

Simple, self-contained auth layer for the demo platform.
Uses hashlib for password hashing and base64-encoded JSON tokens
instead of external JWT libraries.  All user data lives in an
in-memory dict — no database required.
"""

from __future__ import annotations

import base64
import hashlib
import json
import time
from datetime import datetime
from typing import Optional

from fastapi import Depends, Header, HTTPException, status

from models.user import (
    AuthResponse,
    User,
    UserCreate,
    UserLogin,
    UserProfile,
    UserTier,
)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TOKEN_SECRET = "spheres-studio-demo-secret-2026"
TOKEN_EXPIRY_SECONDS = 60 * 60 * 24 * 7  # 7 days


# ---------------------------------------------------------------------------
# Password hashing  (defined early so the seeder can use them)
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    """Hash a plain-text password using SHA-256 with a static salt.

    This is intentionally simple for a demo.  In production you would
    use bcrypt or argon2id with a per-user random salt.
    """
    salted = f"{TOKEN_SECRET}:{password}"
    return hashlib.sha256(salted.encode("utf-8")).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Return True if the plain-text password matches the stored hash."""
    return hash_password(password) == hashed


# ---------------------------------------------------------------------------
# Token creation / verification
# ---------------------------------------------------------------------------

def create_token(user_id: str) -> str:
    """Create a base64-encoded JSON token containing user_id and expiry.

    Format (decoded):  {"uid": "<user_id>", "exp": <unix_timestamp>, "sig": "<hmac>"}
    The signature is a SHA-256 HMAC over uid+exp using the shared secret.
    """
    exp = int(time.time()) + TOKEN_EXPIRY_SECONDS
    payload_str = f"{user_id}:{exp}"
    sig = hashlib.sha256(f"{TOKEN_SECRET}:{payload_str}".encode()).hexdigest()[:32]
    token_data = json.dumps({"uid": user_id, "exp": exp, "sig": sig})
    return base64.urlsafe_b64encode(token_data.encode()).decode()


def verify_token(token: str) -> Optional[str]:
    """Decode and verify a token.  Returns the user_id or None."""
    try:
        decoded = base64.urlsafe_b64decode(token.encode()).decode()
        data = json.loads(decoded)
        uid = data.get("uid", "")
        exp = data.get("exp", 0)
        sig = data.get("sig", "")

        # Check expiry
        if int(time.time()) > exp:
            return None

        # Verify signature
        payload_str = f"{uid}:{exp}"
        expected_sig = hashlib.sha256(
            f"{TOKEN_SECRET}:{payload_str}".encode()
        ).hexdigest()[:32]
        if sig != expected_sig:
            return None

        return uid
    except Exception:
        return None


# ---------------------------------------------------------------------------
# In-memory stores
# ---------------------------------------------------------------------------

_users_by_id: dict[str, User] = {}
_users_by_email: dict[str, User] = {}


def _seed_demo_users() -> None:
    """Pre-populate a handful of demo users for the gallery."""
    demo_accounts = [
        ("Maya Chen", "maya@spheres.city", "demo1234", UserTier.CREATOR),
        ("Jamal Williams", "jamal@spheres.city", "demo1234", UserTier.PRODUCTION),
        ("Sofia Rivera", "sofia@spheres.city", "demo1234", UserTier.STUDIO),
        ("Alex Park", "alex@spheres.city", "demo1234", UserTier.FREE),
        ("Priya Sharma", "priya@spheres.city", "demo1234", UserTier.CREATOR),
    ]
    for name, email, password, tier in demo_accounts:
        if email not in _users_by_email:
            hashed = hash_password(password)
            user = User(
                name=name,
                email=email,
                hashed_password=hashed,
                tier=tier,
                avatar_url=f"https://api.dicebear.com/7.x/initials/svg?seed={name.replace(' ', '+')}",
                designs_count=0,
            )
            _users_by_id[user.id] = user
            _users_by_email[email] = user


# Seed on module import
_seed_demo_users()


# ---------------------------------------------------------------------------
# User CRUD helpers
# ---------------------------------------------------------------------------

def get_user_by_id(user_id: str) -> Optional[User]:
    """Look up a user by their internal ID."""
    return _users_by_id.get(user_id)


def get_user_by_email(email: str) -> Optional[User]:
    """Look up a user by email address."""
    return _users_by_email.get(email.lower().strip())


def register_user(data: UserCreate) -> AuthResponse:
    """Create a new user account and return an auth token.

    Raises HTTPException(409) if the email is already registered.
    """
    if data.email in _users_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        avatar_url=f"https://api.dicebear.com/7.x/initials/svg?seed={data.name.replace(' ', '+')}",
    )
    _users_by_id[user.id] = user
    _users_by_email[user.email] = user

    token = create_token(user.id)
    profile = _user_to_profile(user)
    return AuthResponse(token=token, user=profile)


def login_user(data: UserLogin) -> AuthResponse:
    """Authenticate a user and return an auth token.

    Raises HTTPException(401) on bad credentials.
    """
    user = _users_by_email.get(data.email)
    if user is None or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = create_token(user.id)
    profile = _user_to_profile(user)
    return AuthResponse(token=token, user=profile)


def _user_to_profile(user: User) -> UserProfile:
    """Convert an internal User record to a public UserProfile."""
    return UserProfile(
        id=user.id,
        name=user.name,
        email=user.email,
        avatar_url=user.avatar_url,
        tier=user.tier,
        created_at=user.created_at,
        designs_count=user.designs_count,
    )


# ---------------------------------------------------------------------------
# FastAPI dependency — get_current_user
# ---------------------------------------------------------------------------

async def get_current_user(
    authorization: Optional[str] = Header(default=None),
) -> User:
    """FastAPI dependency that extracts and validates the Bearer token.

    Usage:
        @router.get("/me")
        async def me(user: User = Depends(get_current_user)):
            ...
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization scheme — use 'Bearer <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = verify_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_optional_user(
    authorization: Optional[str] = Header(default=None),
) -> Optional[User]:
    """Like get_current_user but returns None instead of raising 401.

    Useful for endpoints that behave differently for logged-in users
    (e.g. showing whether the current user has voted).
    """
    if not authorization:
        return None
    try:
        return await get_current_user(authorization)
    except HTTPException:
        return None

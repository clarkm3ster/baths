"""
SPHERES Studio — User & Collaboration Models

Pydantic schemas for authentication, sharing, voting, commenting, and teams.
These models define the data layer for the entire collaboration engine.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class UserTier(str, Enum):
    FREE = "free"
    CREATOR = "creator"
    PRODUCTION = "production"
    STUDIO = "studio"


class Visibility(str, Enum):
    PUBLIC = "public"
    UNLISTED = "unlisted"
    PRIVATE = "private"


class TeamRole(str, Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"


class GallerySortOrder(str, Enum):
    NEWEST = "newest"
    MOST_VOTED = "most_voted"
    TRENDING = "trending"
    HIGHEST_PERMANENCE = "highest_permanence"


# ---------------------------------------------------------------------------
# User schemas
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    """Request body for POST /api/auth/register."""
    name: str = Field(..., min_length=1, max_length=100, description="Display name")
    email: str = Field(..., min_length=3, max_length=255, description="Email address")
    password: str = Field(..., min_length=6, max_length=128, description="Plain-text password")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email address")
        return v.lower().strip()

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        return v.strip()


class UserLogin(BaseModel):
    """Request body for POST /api/auth/login."""
    email: str = Field(..., description="Email address")
    password: str = Field(..., description="Plain-text password")

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()


class User(BaseModel):
    """Internal user record stored in the in-memory database."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    name: str
    email: str
    hashed_password: str
    avatar_url: str = ""
    tier: UserTier = UserTier.FREE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    designs_count: int = 0


class UserProfile(BaseModel):
    """Public-facing user profile (no password hash)."""
    id: str
    name: str
    email: str
    avatar_url: str = ""
    tier: UserTier = UserTier.FREE
    created_at: datetime
    designs_count: int = 0


class AuthResponse(BaseModel):
    """Response from login / register."""
    token: str
    user: UserProfile


# ---------------------------------------------------------------------------
# Share link schemas
# ---------------------------------------------------------------------------

class ShareLinkCreate(BaseModel):
    """Request body for POST /api/designs/{id}/share."""
    visibility: Visibility = Visibility.PUBLIC
    expires_hours: Optional[int] = Field(
        default=None,
        ge=1,
        le=8760,
        description="Hours until the share link expires (null = never)",
    )


class ShareLink(BaseModel):
    """A shareable link to a design."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    design_id: str
    owner_id: str
    share_token: str = Field(default_factory=lambda: uuid.uuid4().hex)
    visibility: Visibility = Visibility.PUBLIC
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


class ShareLinkResponse(BaseModel):
    """Response when a share link is created or accessed."""
    share_token: str
    url: str
    visibility: Visibility
    created_at: datetime
    expires_at: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Vote schemas
# ---------------------------------------------------------------------------

class Vote(BaseModel):
    """A single upvote on a design."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    design_id: str
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class VoteResponse(BaseModel):
    """Response for vote endpoints."""
    design_id: str
    vote_count: int
    user_has_voted: bool


# ---------------------------------------------------------------------------
# Comment schemas
# ---------------------------------------------------------------------------

class CommentCreate(BaseModel):
    """Request body for POST /api/designs/{id}/comments."""
    content: str = Field(..., min_length=1, max_length=2000, description="Comment text")
    parent_id: Optional[str] = Field(
        default=None,
        description="ID of parent comment for threading (null = top-level)",
    )

    @field_validator("content")
    @classmethod
    def strip_content(cls, v: str) -> str:
        return v.strip()


class Comment(BaseModel):
    """A comment on a design."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    design_id: str
    user_id: str
    user_name: str = ""
    parent_id: Optional[str] = None
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CommentResponse(BaseModel):
    """A comment with nested replies for threaded display."""
    id: str
    design_id: str
    user_id: str
    user_name: str
    parent_id: Optional[str] = None
    content: str
    created_at: datetime
    updated_at: datetime
    replies: List[CommentResponse] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Team schemas
# ---------------------------------------------------------------------------

class TeamMember(BaseModel):
    """A member within a team."""
    user_id: str
    user_name: str = ""
    user_email: str = ""
    role: TeamRole = TeamRole.VIEWER
    joined_at: datetime = Field(default_factory=datetime.utcnow)


class TeamCreate(BaseModel):
    """Request body for POST /api/teams."""
    name: str = Field(..., min_length=1, max_length=100, description="Team name")

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()


class TeamInvite(BaseModel):
    """Request body for POST /api/teams/{id}/invite."""
    email: str = Field(..., description="Email address of the person to invite")
    role: TeamRole = TeamRole.EDITOR

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()


class Team(BaseModel):
    """A collaborative team."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    name: str
    owner_id: str
    members: List[TeamMember] = Field(default_factory=list)
    design_ids: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TeamResponse(BaseModel):
    """Public team info."""
    id: str
    name: str
    owner_id: str
    members: List[TeamMember]
    created_at: datetime


# ---------------------------------------------------------------------------
# Gallery schemas
# ---------------------------------------------------------------------------

class GalleryDesign(BaseModel):
    """A design card as shown in the public gallery."""
    id: str
    title: str
    author_id: str
    author_name: str
    parcel_id: Optional[str] = None
    parcel_name: Optional[str] = None
    thumbnail_color: str = "#6D28D9"
    element_count: int = 0
    permanence_score: int = 0
    vote_count: int = 0
    comment_count: int = 0
    tags: List[str] = Field(default_factory=list)
    activation_type: Optional[str] = None
    neighborhood: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_featured: bool = False


class GalleryPage(BaseModel):
    """Paginated gallery response."""
    designs: List[GalleryDesign]
    total: int
    page: int
    page_size: int
    total_pages: int


class ForkRequest(BaseModel):
    """Request body for POST /api/designs/{id}/fork."""
    new_title: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Title for the forked copy (default: 'Fork of {original}')",
    )

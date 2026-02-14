"""
SPHERES Studio — Collaboration API Router

All endpoints for auth, sharing, gallery browsing, voting, commenting,
and team management.  Uses in-memory stores so the demo runs without
any external database.
"""

from __future__ import annotations

import math
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from models.user import (
    AuthResponse,
    Comment,
    CommentCreate,
    CommentResponse,
    ForkRequest,
    GalleryDesign,
    GalleryPage,
    GallerySortOrder,
    ShareLink,
    ShareLinkCreate,
    ShareLinkResponse,
    Team,
    TeamCreate,
    TeamInvite,
    TeamMember,
    TeamResponse,
    TeamRole,
    User,
    UserCreate,
    UserLogin,
    UserProfile,
    Visibility,
    Vote,
    VoteResponse,
)
from services.auth import (
    _user_to_profile,
    get_current_user,
    get_optional_user,
    get_user_by_email,
    get_user_by_id,
    login_user,
    register_user,
)

router = APIRouter()


# ---------------------------------------------------------------------------
# In-memory data stores
# ---------------------------------------------------------------------------

_designs: dict[str, GalleryDesign] = {}
_share_links: dict[str, ShareLink] = {}           # keyed by share_token
_share_links_by_design: dict[str, ShareLink] = {}  # keyed by design_id
_votes: dict[str, dict[str, Vote]] = {}            # design_id -> {user_id: Vote}
_comments: dict[str, list[Comment]] = {}           # design_id -> [Comment, ...]
_teams: dict[str, Team] = {}                        # team_id -> Team


def _seed_gallery() -> None:
    """Populate the gallery with sample designs for a rich demo experience."""
    neighborhoods = [
        "Center City", "Fishtown", "Kensington", "West Philadelphia",
        "South Philadelphia", "Northern Liberties", "Germantown",
        "Manayunk", "Old City", "University City",
    ]
    activation_types = ["single_day", "weekend", "week", "month", "ongoing"]
    tag_pool = [
        "community", "garden", "music", "art", "food", "wellness",
        "youth", "sustainability", "heritage", "innovation", "play",
        "market", "performance", "nature", "education",
    ]
    colors = [
        "#6D28D9", "#8B5CF6", "#EC4899", "#F59E0B", "#22C55E",
        "#3B82F6", "#EF4444", "#06B6D4", "#16A34A", "#D97706",
        "#7C3AED", "#DB2777", "#1D4ED8", "#15803D", "#BE185D",
    ]

    # Map demo user emails to their IDs
    from services.auth import _users_by_email

    demo_users = list(_users_by_email.values())
    if not demo_users:
        return

    sample_designs = [
        ("Kensington Green Revival", "A community garden and native meadow transforming a vacant lot into a neighborhood gathering space"),
        ("Fishtown Friday Nights", "Weekly live music series with food trucks and local craft vendors along Frankford Ave"),
        ("West Philly Art Walk", "Interactive art installations along Baltimore Ave with mural walls and sculpture pads"),
        ("South Philly Bocce League", "Permanent bocce courts with seating and shade structures in Marconi Plaza"),
        ("Old City Light Festival", "Projection mapping and LED art installations throughout historic Old City alleyways"),
        ("Germantown Harvest Market", "Seasonal farmers market with community kitchen and nutrition workshops"),
        ("Northern Liberties Play Park", "Adventure playground with natural play structures and water features"),
        ("University City Innovation Hub", "Outdoor co-working space with wifi, power hookups, and community programming"),
        ("Manayunk Trail Fitness", "Outdoor fitness stations along the towpath with group exercise programming"),
        ("Center City Pocket Oasis", "Miniature park with native plantings, a small fountain, and chess tables"),
        ("Strawberry Mansion Stage", "Community amphitheater with year-round performance programming"),
        ("Point Breeze Block Party", "Monthly block party series celebrating local culture with DJs and food carts"),
        ("Passyunk Pollinator Path", "Butterfly garden corridor connecting three vacant lots along Passyunk Ave"),
        ("Brewerytown Mural Mile", "Walking trail connecting twelve new community murals with wayfinding signage"),
        ("Cedar Park Cinema", "Outdoor screening wall with bleacher seating for weekend movie nights"),
        ("Grays Ferry Skate Spot", "Community-designed skate park with spectator seating and shade sails"),
        ("Chinatown Heritage Garden", "Traditional Chinese garden with pavilion, moon gate, and meditation space"),
        ("Cobbs Creek Nature Play", "Nature-based play area using fallen trees, boulders, and native plantings"),
        ("Tacony Music Pavilion", "Permanent bandshell with sound equipment and tiered lawn seating"),
        ("East Falls Farmers Circle", "Year-round indoor/outdoor market pavilion with raised beds and greenhouse"),
    ]

    for i, (title, description) in enumerate(sample_designs):
        author = demo_users[i % len(demo_users)]
        neighborhood = neighborhoods[i % len(neighborhoods)]
        n_tags = random.randint(2, 5)
        tags = random.sample(tag_pool, n_tags)
        design = GalleryDesign(
            id=uuid.uuid4().hex[:16],
            title=title,
            author_id=author.id,
            author_name=author.name,
            parcel_id=f"PHL-{random.randint(1000, 9999)}",
            parcel_name=f"{neighborhood} Parcel {random.randint(1, 50)}",
            thumbnail_color=colors[i % len(colors)],
            element_count=random.randint(3, 18),
            permanence_score=random.randint(15, 95),
            vote_count=random.randint(0, 120),
            comment_count=random.randint(0, 25),
            tags=tags,
            activation_type=activation_types[i % len(activation_types)],
            neighborhood=neighborhood,
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 90)),
            is_featured=i < 5,
        )
        _designs[design.id] = design
        author.designs_count += 1

        # Seed some votes
        for _ in range(design.vote_count):
            voter = random.choice(demo_users)
            if design.id not in _votes:
                _votes[design.id] = {}
            if voter.id not in _votes[design.id]:
                _votes[design.id][voter.id] = Vote(
                    design_id=design.id,
                    user_id=voter.id,
                )

        # Seed some comments
        sample_comments_text = [
            "Love this concept! The permanence score is impressive.",
            "How did you handle the permit requirements for the sound equipment?",
            "This would work great in our neighborhood too.",
            "Beautiful layout. The native plantings are a nice touch.",
            "Can we collaborate on something similar for our block?",
            "The cost estimate seems very reasonable for what you get.",
            "I voted for this one. Hope it gets built!",
            "Great use of the space. The seating arrangement is clever.",
        ]
        _comments[design.id] = []
        for j in range(min(design.comment_count, 4)):
            commenter = random.choice(demo_users)
            comment = Comment(
                design_id=design.id,
                user_id=commenter.id,
                user_name=commenter.name,
                content=sample_comments_text[j % len(sample_comments_text)],
                created_at=datetime.utcnow() - timedelta(
                    days=random.randint(0, 30),
                    hours=random.randint(0, 23),
                ),
            )
            _comments[design.id].append(comment)


# Seed gallery on module import
_seed_gallery()


# ═══════════════════════════════════════════════════════════════════════════
# AUTH ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@router.post("/api/auth/register", response_model=AuthResponse, status_code=201)
async def api_register(data: UserCreate) -> AuthResponse:
    """Create a new user account."""
    return register_user(data)


@router.post("/api/auth/login", response_model=AuthResponse)
async def api_login(data: UserLogin) -> AuthResponse:
    """Authenticate and receive a bearer token."""
    return login_user(data)


@router.get("/api/auth/me", response_model=UserProfile)
async def api_me(user: User = Depends(get_current_user)) -> UserProfile:
    """Return the profile of the currently authenticated user."""
    return _user_to_profile(user)


# ═══════════════════════════════════════════════════════════════════════════
# SHARE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@router.post(
    "/api/designs/{design_id}/share",
    response_model=ShareLinkResponse,
    status_code=201,
)
async def api_share_design(
    design_id: str,
    data: ShareLinkCreate,
    user: User = Depends(get_current_user),
) -> ShareLinkResponse:
    """Generate a shareable link for a design."""
    expires_at = None
    if data.expires_hours is not None:
        expires_at = datetime.utcnow() + timedelta(hours=data.expires_hours)

    link = ShareLink(
        design_id=design_id,
        owner_id=user.id,
        visibility=data.visibility,
        expires_at=expires_at,
    )
    _share_links[link.share_token] = link
    _share_links_by_design[design_id] = link

    # If the design exists in our gallery, update its visibility implicitly
    if design_id in _designs and data.visibility == Visibility.PUBLIC:
        pass  # already public

    return ShareLinkResponse(
        share_token=link.share_token,
        url=f"/shared/{link.share_token}",
        visibility=link.visibility,
        created_at=link.created_at,
        expires_at=link.expires_at,
    )


@router.get("/api/designs/shared/{share_token}", response_model=GalleryDesign)
async def api_get_shared_design(share_token: str) -> GalleryDesign:
    """Access a design via its share token."""
    link = _share_links.get(share_token)
    if link is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share link not found",
        )

    # Check expiry
    if link.expires_at and datetime.utcnow() > link.expires_at:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="This share link has expired",
        )

    design = _designs.get(link.design_id)
    if design is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found",
        )

    return design


@router.post("/api/designs/{design_id}/fork", response_model=GalleryDesign, status_code=201)
async def api_fork_design(
    design_id: str,
    data: ForkRequest,
    user: User = Depends(get_current_user),
) -> GalleryDesign:
    """Copy a design to the current user's account."""
    original = _designs.get(design_id)
    if original is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found",
        )

    fork_title = data.new_title if data.new_title else f"Fork of {original.title}"
    forked = GalleryDesign(
        id=uuid.uuid4().hex[:16],
        title=fork_title,
        author_id=user.id,
        author_name=user.name,
        parcel_id=original.parcel_id,
        parcel_name=original.parcel_name,
        thumbnail_color=original.thumbnail_color,
        element_count=original.element_count,
        permanence_score=original.permanence_score,
        vote_count=0,
        comment_count=0,
        tags=list(original.tags) + ["forked"],
        activation_type=original.activation_type,
        neighborhood=original.neighborhood,
        created_at=datetime.utcnow(),
        is_featured=False,
    )

    _designs[forked.id] = forked
    user.designs_count += 1

    return forked


# ═══════════════════════════════════════════════════════════════════════════
# GALLERY ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/api/gallery", response_model=GalleryPage)
async def api_gallery(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=100),
    sort: GallerySortOrder = Query(default=GallerySortOrder.NEWEST),
    activation_type: Optional[str] = Query(default=None),
    neighborhood: Optional[str] = Query(default=None),
    tag: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
) -> GalleryPage:
    """Browse public designs with filtering, sorting, and pagination."""
    designs = list(_designs.values())

    # --- Filters ---
    if activation_type:
        designs = [d for d in designs if d.activation_type == activation_type]
    if neighborhood:
        designs = [d for d in designs if d.neighborhood and neighborhood.lower() in d.neighborhood.lower()]
    if tag:
        designs = [d for d in designs if tag.lower() in [t.lower() for t in d.tags]]
    if search:
        q = search.lower()
        designs = [
            d for d in designs
            if q in d.title.lower()
            or q in d.author_name.lower()
            or q in (d.neighborhood or "").lower()
            or any(q in t.lower() for t in d.tags)
        ]

    # --- Sort ---
    if sort == GallerySortOrder.NEWEST:
        designs.sort(key=lambda d: d.created_at, reverse=True)
    elif sort == GallerySortOrder.MOST_VOTED:
        designs.sort(key=lambda d: d.vote_count, reverse=True)
    elif sort == GallerySortOrder.TRENDING:
        # Trending = votes / age_in_hours  (Wilson-score-like approximation)
        now = datetime.utcnow()
        def trending_score(d: GalleryDesign) -> float:
            age_hours = max((now - d.created_at).total_seconds() / 3600, 1)
            return d.vote_count / math.log2(age_hours + 2)
        designs.sort(key=trending_score, reverse=True)
    elif sort == GallerySortOrder.HIGHEST_PERMANENCE:
        designs.sort(key=lambda d: d.permanence_score, reverse=True)

    # --- Paginate ---
    total = len(designs)
    total_pages = max(math.ceil(total / page_size), 1)
    start = (page - 1) * page_size
    end = start + page_size
    page_designs = designs[start:end]

    return GalleryPage(
        designs=page_designs,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/api/gallery/featured", response_model=List[GalleryDesign])
async def api_gallery_featured() -> List[GalleryDesign]:
    """Return featured / trending designs for the hero section."""
    featured = [d for d in _designs.values() if d.is_featured]
    if not featured:
        # Fall back to top voted
        all_designs = sorted(
            _designs.values(),
            key=lambda d: d.vote_count,
            reverse=True,
        )
        featured = all_designs[:5]
    return featured


@router.get("/api/gallery/parcel/{parcel_id}", response_model=List[GalleryDesign])
async def api_gallery_by_parcel(parcel_id: str) -> List[GalleryDesign]:
    """Return all designs associated with a specific parcel."""
    return [d for d in _designs.values() if d.parcel_id == parcel_id]


# ═══════════════════════════════════════════════════════════════════════════
# VOTE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@router.post("/api/designs/{design_id}/vote", response_model=VoteResponse)
async def api_toggle_vote(
    design_id: str,
    user: User = Depends(get_current_user),
) -> VoteResponse:
    """Toggle an upvote on a design (vote if not voted, un-vote if already voted)."""
    if design_id not in _votes:
        _votes[design_id] = {}

    user_voted = user.id in _votes[design_id]

    if user_voted:
        # Remove vote
        del _votes[design_id][user.id]
        if design_id in _designs:
            _designs[design_id].vote_count = max(0, _designs[design_id].vote_count - 1)
    else:
        # Add vote
        _votes[design_id][user.id] = Vote(design_id=design_id, user_id=user.id)
        if design_id in _designs:
            _designs[design_id].vote_count += 1

    count = len(_votes[design_id])
    return VoteResponse(
        design_id=design_id,
        vote_count=count,
        user_has_voted=not user_voted,
    )


@router.get("/api/designs/{design_id}/votes", response_model=VoteResponse)
async def api_get_votes(
    design_id: str,
    user: Optional[User] = Depends(get_optional_user),
) -> VoteResponse:
    """Get the vote count for a design and whether the current user has voted."""
    votes = _votes.get(design_id, {})
    user_has_voted = user is not None and user.id in votes
    return VoteResponse(
        design_id=design_id,
        vote_count=len(votes),
        user_has_voted=user_has_voted,
    )


# ═══════════════════════════════════════════════════════════════════════════
# COMMENT ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

def _build_threaded_comments(design_id: str) -> List[CommentResponse]:
    """Organize flat comment list into a threaded tree."""
    flat = _comments.get(design_id, [])
    comment_map: dict[str, CommentResponse] = {}
    roots: list[CommentResponse] = []

    # First pass: create response objects
    for c in flat:
        cr = CommentResponse(
            id=c.id,
            design_id=c.design_id,
            user_id=c.user_id,
            user_name=c.user_name,
            parent_id=c.parent_id,
            content=c.content,
            created_at=c.created_at,
            updated_at=c.updated_at,
            replies=[],
        )
        comment_map[c.id] = cr

    # Second pass: nest replies under parents
    for cr in comment_map.values():
        if cr.parent_id and cr.parent_id in comment_map:
            comment_map[cr.parent_id].replies.append(cr)
        else:
            roots.append(cr)

    # Sort roots and replies by date
    roots.sort(key=lambda c: c.created_at)
    for cr in comment_map.values():
        cr.replies.sort(key=lambda c: c.created_at)

    return roots


@router.post(
    "/api/designs/{design_id}/comments",
    response_model=CommentResponse,
    status_code=201,
)
async def api_add_comment(
    design_id: str,
    data: CommentCreate,
    user: User = Depends(get_current_user),
) -> CommentResponse:
    """Add a comment to a design."""
    if design_id not in _comments:
        _comments[design_id] = []

    # If replying, verify parent exists
    if data.parent_id:
        parent_exists = any(c.id == data.parent_id for c in _comments[design_id])
        if not parent_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent comment not found",
            )

    comment = Comment(
        design_id=design_id,
        user_id=user.id,
        user_name=user.name,
        parent_id=data.parent_id,
        content=data.content,
    )
    _comments[design_id].append(comment)

    # Update comment count on the design
    if design_id in _designs:
        _designs[design_id].comment_count += 1

    return CommentResponse(
        id=comment.id,
        design_id=comment.design_id,
        user_id=comment.user_id,
        user_name=comment.user_name,
        parent_id=comment.parent_id,
        content=comment.content,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        replies=[],
    )


@router.get(
    "/api/designs/{design_id}/comments",
    response_model=List[CommentResponse],
)
async def api_get_comments(design_id: str) -> List[CommentResponse]:
    """Get threaded comments for a design."""
    return _build_threaded_comments(design_id)


@router.delete("/api/comments/{comment_id}", status_code=204)
async def api_delete_comment(
    comment_id: str,
    user: User = Depends(get_current_user),
) -> None:
    """Delete your own comment."""
    for design_id, comment_list in _comments.items():
        for i, comment in enumerate(comment_list):
            if comment.id == comment_id:
                if comment.user_id != user.id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You can only delete your own comments",
                    )
                comment_list.pop(i)
                # Also remove any replies to this comment
                _comments[design_id] = [
                    c for c in comment_list
                    if c.parent_id != comment_id
                ]
                # Update count
                if design_id in _designs:
                    _designs[design_id].comment_count = len(_comments[design_id])
                return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Comment not found",
    )


# ═══════════════════════════════════════════════════════════════════════════
# TEAM ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@router.post("/api/teams", response_model=TeamResponse, status_code=201)
async def api_create_team(
    data: TeamCreate,
    user: User = Depends(get_current_user),
) -> TeamResponse:
    """Create a new team with the current user as owner."""
    owner_member = TeamMember(
        user_id=user.id,
        user_name=user.name,
        user_email=user.email,
        role=TeamRole.OWNER,
    )

    team = Team(
        name=data.name,
        owner_id=user.id,
        members=[owner_member],
    )
    _teams[team.id] = team

    return TeamResponse(
        id=team.id,
        name=team.name,
        owner_id=team.owner_id,
        members=team.members,
        created_at=team.created_at,
    )


@router.post("/api/teams/{team_id}/invite", response_model=TeamResponse)
async def api_invite_member(
    team_id: str,
    data: TeamInvite,
    user: User = Depends(get_current_user),
) -> TeamResponse:
    """Invite a user to a team by email."""
    team = _teams.get(team_id)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )

    # Only owner or editors can invite
    caller_member = next(
        (m for m in team.members if m.user_id == user.id),
        None,
    )
    if caller_member is None or caller_member.role == TeamRole.VIEWER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to invite members to this team",
        )

    # Check if invitee is already a member
    if any(m.user_email == data.email for m in team.members):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user is already a team member",
        )

    # Look up the user
    invitee = get_user_by_email(data.email)
    if invitee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account found with that email address",
        )

    new_member = TeamMember(
        user_id=invitee.id,
        user_name=invitee.name,
        user_email=invitee.email,
        role=data.role,
    )
    team.members.append(new_member)

    return TeamResponse(
        id=team.id,
        name=team.name,
        owner_id=team.owner_id,
        members=team.members,
        created_at=team.created_at,
    )


@router.get("/api/teams/{team_id}/members", response_model=List[TeamMember])
async def api_get_team_members(
    team_id: str,
    user: User = Depends(get_current_user),
) -> List[TeamMember]:
    """List members of a team."""
    team = _teams.get(team_id)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )

    # Verify caller is a member
    if not any(m.user_id == user.id for m in team.members):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this team",
        )

    return team.members


@router.get("/api/teams/{team_id}/designs", response_model=List[GalleryDesign])
async def api_get_team_designs(
    team_id: str,
    user: User = Depends(get_current_user),
) -> List[GalleryDesign]:
    """Get all designs belonging to team members."""
    team = _teams.get(team_id)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )

    if not any(m.user_id == user.id for m in team.members):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this team",
        )

    member_ids = {m.user_id for m in team.members}
    team_designs = [
        d for d in _designs.values()
        if d.author_id in member_ids
    ]
    team_designs.sort(key=lambda d: d.created_at, reverse=True)

    return team_designs

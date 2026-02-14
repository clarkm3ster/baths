"""
SPHERES — Episode API Routes
==============================
Three endpoints. Ten episodes. Every dormant space in Philadelphia.
"""

from fastapi import APIRouter, HTTPException
from models.episodes import (
    Episode,
    EpisodeSummary,
    EpisodeStats,
    get_episode_summaries,
    get_episode_by_slug,
    get_episode_stats,
)

router = APIRouter(prefix="/api/episodes", tags=["episodes"])


@router.get("", response_model=list[EpisodeSummary])
def list_episodes():
    """
    Return all 10 episodes in summary view.

    Summary includes: id, slug, title, subtitle, location, neighborhood,
    genre, genre_color, color_palette, estimated_cost, permanence_percentage.
    """
    return get_episode_summaries()


@router.get("/stats", response_model=EpisodeStats)
def episodes_stats():
    """
    Return aggregate statistics across all episodes.

    Includes: total cost range, total jobs created, total people served,
    average permanence percentage, list of neighborhoods and genres.
    """
    return get_episode_stats()


@router.get("/{slug}", response_model=Episode)
def get_episode(slug: str):
    """
    Return full detail for a single episode by its URL slug.

    Slugs: waterfront, vacant-lot, rooftop, alley, park, underpass,
    market, plaza, corridor, garden.
    """
    episode = get_episode_by_slug(slug)
    if episode is None:
        raise HTTPException(
            status_code=404,
            detail=f"Episode with slug '{slug}' not found. "
            f"Valid slugs: waterfront, vacant-lot, rooftop, alley, park, "
            f"underpass, market, plaza, corridor, garden.",
        )
    return episode

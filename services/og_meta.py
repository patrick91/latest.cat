"""Centralized Open Graph metadata configuration.

This module ensures OG tags stay in sync between server, templates, and image generation.
"""

from typing import TypedDict


class OGMeta(TypedDict):
    """Open Graph metadata structure"""

    title: str
    description: str
    url: str
    image: str


# Site-wide OG metadata constants
SITE_NAME = "latest.cat 🐱"
SITE_TAGLINE = "check latest versions of your favorite software"
SITE_DESCRIPTION = "Check the latest versions of your favorite programming languages, frameworks, and tools"

# OG Image dimensions (standard size)
OG_IMAGE_WIDTH = 1200
OG_IMAGE_HEIGHT = 630


def get_home_og_meta(base_url: str) -> OGMeta:
    """Get OG metadata for the home page"""
    return {
        "title": f"{SITE_NAME} - {SITE_TAGLINE}",
        "description": SITE_DESCRIPTION,
        "url": f"{base_url}/",
        "image": f"{base_url}/static/social-card.png",
    }


def get_software_og_meta(
    base_url: str, path: str, software_name: str, software_slug: str, version: str
) -> OGMeta:
    """Get OG metadata for a software page"""
    return {
        "title": f"{software_name} {version} - {SITE_NAME}",
        "description": f"The latest version of {software_name} is {version}",
        "url": f"{base_url}{path}",
        "image": f"{base_url}/og-image/{software_slug}.png",
    }

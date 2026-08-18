import re

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SLUG_MIN_LENGTH = 2
SLUG_MAX_LENGTH = 63

RESERVED_SLUGS = frozenset(
    {
        "www",
        "app",
        "api",
        "mail",
        "status",
        "admin",
        "localhost",
    }
)


def normalize_slug(value: str) -> str:
    return value.strip().lower()


def validate_slug(value: str) -> str:
    slug = normalize_slug(value)
    if not SLUG_MIN_LENGTH <= len(slug) <= SLUG_MAX_LENGTH:
        raise ValueError("Slug must be between 2 and 63 characters")
    if not SLUG_PATTERN.fullmatch(slug):
        raise ValueError("Slug must be lowercase letters, numbers, and hyphens")
    if slug in RESERVED_SLUGS:
        raise ValueError("This slug is reserved")
    return slug

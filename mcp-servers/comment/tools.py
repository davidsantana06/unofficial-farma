from typing import Optional

from client import request, compose_search_params
from models import Comment


def check_comment_service_health() -> dict[str, str]:
    """Check that the comment service is reachable and answering requests.

    Use this to tell a service outage apart from a search that simply found
    nothing.

    Returns:
        The reported status, such as {"status": "ok", "service": "comment"}.
    """
    return request("GET", "/health")


def list_comments(limit: int = 50, offset: int = 0) -> list[Comment]:
    """List customer reviews left on medicines in Unofficial Farma.

    Returns comments in insertion order, across every product and without any
    filtering, so read product_id on each item to know which medicine it refers
    to. Use search_comments instead to read the reviews of one medicine.

    Args:
        limit: Maximum number of comments to return.
        offset: How many comments to skip, for pagination.

    Returns:
        The comments found, each with its id, reviewed product_id, author name
        and email, content and timestamps. Empty when the offset goes past the
        last comment.
    """
    payload = request("GET", "/comments", params={"limit": limit, "offset": offset})
    return [Comment.model_validate(item) for item in payload]


def search_comments(
    product_id: Optional[int] = None,
    author_name: Optional[str] = None,
    author_email: Optional[str] = None,
    content: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Comment]:
    """Search customer reviews by medicine, author or wording.

    Filters combine with AND, so passing several narrows the result. The text
    filters (author_name, author_email, content) are case-insensitive partial
    matches, so "dor" finds every review mentioning it. product_id is an exact
    match and is the usual way to read the reviews of one medicine. Omitting
    every filter returns all comments, exactly like list_comments.

    Args:
        product_id: Return only reviews written about this medicine.
        author_name: Text to look for anywhere in the reviewer's name.
        author_email: Text to look for anywhere in the reviewer's email.
        content: Text to look for anywhere in the body of the review.
        limit: Maximum number of comments to return.
        offset: How many comments to skip, for pagination.

    Returns:
        The matching comments, each with its id, reviewed product_id, author
        name and email, content and timestamps. Empty when nothing matches.
    """
    filters = {
        "product_id": product_id,
        "author_name": author_name,
        "author_email": author_email,
        "content": content,
    }
    payload = request(
        "GET",
        "/comments/search",
        params=compose_search_params(filters, limit, offset),
    )
    return [Comment.model_validate(item) for item in payload]

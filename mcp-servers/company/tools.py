from typing import Optional

from client import request, compose_search_params
from models import Company


def check_company_service_health() -> dict[str, str]:
    """Check that the company service is reachable and answering requests.

    Use this to tell a service outage apart from a search that simply found
    nothing.

    Returns:
        The reported status, such as {"status": "ok", "service": "company"}.
    """
    return request("GET", "/health")


def list_companies(limit: int = 50, offset: int = 0) -> list[Company]:
    """List the pharmaceutical companies registered in Unofficial Farma.

    Returns companies in insertion order, without any filtering. Use this to
    browse the whole catalogue or to page through it; use search_companies
    instead when looking for a company by name.

    Args:
        limit: Maximum number of companies to return.
        offset: How many companies to skip, for pagination.

    Returns:
        The companies found, each with its id, name and timestamps. Empty when
        the offset goes past the last company.
    """
    payload = request("GET", "/companies", params={"limit": limit, "offset": offset})
    return [Company.model_validate(item) for item in payload]


def search_companies(
    name: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Company]:
    """Search pharmaceutical companies by name.

    The name filter is a case-insensitive partial match, so "vale" matches
    "Laboratório Vale Verde". Omitting it returns every company, exactly like
    list_companies.

    Args:
        name: Text to look for anywhere in the company name.
        limit: Maximum number of companies to return.
        offset: How many companies to skip, for pagination.

    Returns:
        The matching companies, each with its id, name and timestamps. Empty
        when nothing matches.
    """
    filters = {"name": name}
    payload = request(
        "GET",
        "/companies/search",
        params=compose_search_params(filters, limit, offset),
    )
    return [Company.model_validate(item) for item in payload]

from typing import Optional

from client import request, compose_search_params
from models import Product


def check_product_service_health() -> dict[str, str]:
    """Check that the product service is reachable and answering requests.

    Use this to tell a service outage apart from a search that simply found
    nothing.

    Returns:
        The reported status, such as {"status": "ok", "service": "product"}.
    """
    return request("GET", "/health")


def list_products(limit: int = 50, offset: int = 0) -> list[Product]:
    """List the medicines registered in Unofficial Farma.

    Returns products in insertion order, without any filtering. Use this to
    browse the whole catalogue or to page through it; use search_products
    instead when looking for medicines by name, maker, dosage or price.

    Args:
        limit: Maximum number of products to return.
        offset: How many products to skip, for pagination.

    Returns:
        The products found, each with its id, owning company_id, name,
        description, price in BRL, dosage and timestamps. Empty when the offset
        goes past the last product.
    """
    payload = request("GET", "/products", params={"limit": limit, "offset": offset})
    return [Product.model_validate(item) for item in payload]


def search_products(
    company_id: Optional[int] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    dosage: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Product]:
    """Search medicines by maker, name, description, price or dosage.

    Filters combine with AND, so passing several narrows the result. The text
    filters (name, description, dosage) are case-insensitive partial matches,
    so "ibup" matches "Ibuprofeno". company_id and price are exact matches:
    price will not find a range, only medicines costing that precise amount.
    Omitting every filter returns all products, exactly like list_products.

    Args:
        company_id: Return only medicines made by this company.
        name: Text to look for anywhere in the commercial name.
        description: Text to look for anywhere in the description.
        price: Exact retail price in BRL, such as 12.90.
        dosage: Text to look for anywhere in the dosage, such as "500 mg".
        limit: Maximum number of products to return.
        offset: How many products to skip, for pagination.

    Returns:
        The matching products, each with its id, owning company_id, name,
        description, price in BRL, dosage and timestamps. Empty when nothing
        matches.
    """
    filters = {
        "company_id": company_id,
        "name": name,
        "description": description,
        "price": price,
        "dosage": dosage,
    }
    payload = request(
        "GET",
        "/products/search",
        params=compose_search_params(filters, limit, offset),
    )
    return [Product.model_validate(item) for item in payload]

from fastmcp import FastMCP

from tools import check_product_service_health, list_products, search_products

mcp = FastMCP(
    "unofficial-farma-product",
    tools=[check_product_service_health, list_products, search_products],
)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=9002)

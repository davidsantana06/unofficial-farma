from fastmcp import FastMCP

from tools import check_company_service_health, list_companies, search_companies

mcp = FastMCP(
    "unofficial-farma-company",
    tools=[check_company_service_health, list_companies, search_companies],
)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=9001)

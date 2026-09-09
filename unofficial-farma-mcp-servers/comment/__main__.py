from fastmcp import FastMCP

from tools import check_comment_service_health, list_comments, search_comments

mcp = FastMCP(
    "unofficial-farma-comment",
    tools=[check_comment_service_health, list_comments, search_comments],
)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=9001)

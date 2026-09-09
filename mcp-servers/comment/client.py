from fastmcp.exceptions import ToolError
from httpx import RequestError, Response
from typing import Any, Literal
import httpx

_SERVICE_NAME = "comment"
_SERVICE_URL = "http://unofficial-farma-comment-service:8003"
_REQUEST_TIMEOUT_IN_SECONDS = 10


def _compose_error_message(response: Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return response.text.strip() or "empty response body"
    if isinstance(body, dict) and "detail" in body:
        return str(body["detail"])
    return str(body)


def request(
    method: Literal["GET", "POST", "PATCH", "DELETE"],
    path: str,
    **kwargs: Any,
) -> Any:
    try:
        response = httpx.request(
            method,
            f"{_SERVICE_URL}{path}",
            timeout=_REQUEST_TIMEOUT_IN_SECONDS,
            **kwargs,
        )
    except RequestError as error:
        raise ToolError(
            f"could not reach the {_SERVICE_NAME} service at {_SERVICE_URL}: {error}"
        ) from error
    if response.is_error:
        raise ToolError(
            f"{_SERVICE_NAME} service returned {response.status_code} for "
            f"{method} {path}: {_compose_error_message(response)}"
        )
    return response.json()


def compose_search_params(
    filters: dict[str, Any], limit: int, offset: int
) -> dict[str, Any]:
    params = {key: value for key, value in filters.items() if value is not None}
    params["limit"] = limit
    params["offset"] = offset
    return params

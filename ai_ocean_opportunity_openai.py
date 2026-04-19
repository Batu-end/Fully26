from __future__ import annotations

import json
import os
from typing import Any, TypeVar

from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()

SchemaT = TypeVar("SchemaT", bound=BaseModel)

_openai_client: Any | None = None


class OceanOpportunityOpenAIError(RuntimeError):
    """Base error for shared OpenAI helper failures."""


class OpenAIConfigError(OceanOpportunityOpenAIError):
    """Raised when required OpenAI environment configuration is missing."""


class OpenAIDependencyError(OceanOpportunityOpenAIError):
    """Raised when the OpenAI SDK is not installed in the environment."""


class OpenAIRequestError(OceanOpportunityOpenAIError):
    """Raised when the SDK call fails before a usable response is returned."""


class OpenAIResponseError(OceanOpportunityOpenAIError):
    """Raised when the model response is incomplete, refused, or invalid JSON."""


def resolve_openai_api_key() -> str:
    """Return the configured OpenAI API key or fail with a predictable error."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise OpenAIConfigError(
            "OPENAI_API_KEY is not set. Add it to the environment before making AI calls."
        )
    return api_key


def resolve_openai_model() -> str:
    """Return the configured OpenAI model name or fail with a predictable error."""

    model = os.getenv("OPENAI_MODEL")
    if not model:
        raise OpenAIConfigError(
            "OPENAI_MODEL is not set. Add it to the environment before making AI calls."
        )
    return model


def get_openai_client() -> Any:
    """Create and cache a shared OpenAI client for this process."""

    global _openai_client

    if _openai_client is not None:
        return _openai_client

    api_key = resolve_openai_api_key()

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise OpenAIDependencyError(
            "The 'openai' package is not installed. Install the OpenAI Python SDK "
            "before using the AI Ocean Opportunity helper."
        ) from exc

    _openai_client = OpenAI(api_key=api_key)
    return _openai_client


def call_openai_json(
    *,
    system_prompt: str,
    user_prompt: str | None = None,
    input_items: list[dict[str, Any]] | None = None,
    output_model: type[SchemaT] | None = None,
    model: str | None = None,
) -> SchemaT | dict[str, Any]:
    """Make one JSON-oriented model call and return parsed structured output.

    When ``output_model`` is provided, the helper prefers SDK-backed structured
    parsing and falls back to JSON mode plus Pydantic validation if needed.
    """

    if not system_prompt.strip():
        raise OpenAIRequestError("system_prompt must not be empty.")

    prompt_items = _build_input_items(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        input_items=input_items,
        require_json_instruction=output_model is None,
    )

    client = get_openai_client()
    resolved_model = model or resolve_openai_model()

    try:
        if output_model is not None and hasattr(client.responses, "parse"):
            response = client.responses.parse(
                model=resolved_model,
                input=prompt_items,
                text_format=output_model,
            )
            _raise_for_response_issues(response)

            parsed = getattr(response, "output_parsed", None)
            if parsed is None:
                raise OpenAIResponseError(
                    "OpenAI returned no parsed structured output for the requested schema."
                )
            return parsed

        response = client.responses.create(
            model=resolved_model,
            input=prompt_items,
            text={"format": {"type": "json_object"}},
        )
    except OceanOpportunityOpenAIError:
        raise
    except Exception as exc:
        raise OpenAIRequestError(f"OpenAI request failed: {exc}") from exc

    _raise_for_response_issues(response)

    parsed_json = _parse_json_output(response)
    if output_model is None:
        return parsed_json
    return _validate_with_model(output_model, parsed_json)


def _build_input_items(
    *,
    system_prompt: str,
    user_prompt: str | None,
    input_items: list[dict[str, Any]] | None,
    require_json_instruction: bool,
) -> list[dict[str, Any]]:
    if input_items is not None and user_prompt is not None:
        raise OpenAIRequestError(
            "Provide either user_prompt or input_items, not both, when calling the OpenAI helper."
        )

    system_content = system_prompt.strip()
    if require_json_instruction and "json" not in system_content.lower():
        system_content = f"{system_content}\n\nReturn valid JSON only."

    items: list[dict[str, Any]] = [{"role": "system", "content": system_content}]

    if input_items is not None:
        items.extend(input_items)
        return items

    if user_prompt is None or not user_prompt.strip():
        raise OpenAIRequestError(
            "Either user_prompt or input_items must provide user content for the model call."
        )

    items.append({"role": "user", "content": user_prompt.strip()})
    return items


def _raise_for_response_issues(response: Any) -> None:
    status = getattr(response, "status", None)
    if status == "incomplete":
        incomplete_details = getattr(response, "incomplete_details", None)
        reason = getattr(incomplete_details, "reason", None)
        if reason is None and isinstance(incomplete_details, dict):
            reason = incomplete_details.get("reason")
        raise OpenAIResponseError(
            f"OpenAI response was incomplete: {reason or 'unknown'}"
        )

    refusal = _extract_refusal(response)
    if refusal:
        raise OpenAIResponseError(f"OpenAI refused the request: {refusal}")


def _extract_refusal(response: Any) -> str | None:
    for output_item in getattr(response, "output", []) or []:
        for content_item in _get_content_items(output_item):
            item_type = _get_attr_or_key(content_item, "type")
            if item_type == "refusal":
                refusal = _get_attr_or_key(content_item, "refusal")
                return refusal or "Request refused."
    return None


def _parse_json_output(response: Any) -> dict[str, Any]:
    raw_text = getattr(response, "output_text", None)
    if raw_text is None:
        raw_text = _extract_output_text(response)

    if not raw_text:
        raise OpenAIResponseError("OpenAI returned no JSON text output to parse.")

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise OpenAIResponseError(f"OpenAI returned invalid JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise OpenAIResponseError(
            "OpenAI JSON output must be an object at the top level."
        )

    return parsed


def _extract_output_text(response: Any) -> str | None:
    for output_item in getattr(response, "output", []) or []:
        for content_item in _get_content_items(output_item):
            item_type = _get_attr_or_key(content_item, "type")
            if item_type == "output_text":
                text = _get_attr_or_key(content_item, "text")
                return text
    return None


def _get_content_items(output_item: Any) -> list[Any]:
    content_items = _get_attr_or_key(output_item, "content")
    if content_items is None:
        return []
    return list(content_items)


def _get_attr_or_key(item: Any, key: str) -> Any:
    value = getattr(item, key, None)
    if value is None and isinstance(item, dict):
        return item.get(key)
    return value


def _validate_with_model(
    output_model: type[SchemaT], parsed_json: dict[str, Any]
) -> SchemaT:
    if hasattr(output_model, "model_validate"):
        return output_model.model_validate(parsed_json)
    return output_model.parse_obj(parsed_json)

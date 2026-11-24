import json
from typing import Any


def normalize_arguments(arguments: dict) -> dict:
    """Remove optional arguments whose value is None."""
    return {
        key: value
        for key, value in arguments.items()
        if value is not None
    }


def parse_tool_result(content: Any) -> dict | None:
    """Convert a tool message's content into a dictionary."""
    if isinstance(content, dict):
        return content

    if isinstance(content, str):
        try:
            result = json.loads(content)
            return result if isinstance(result, dict) else None
        except json.JSONDecodeError:
            return None

    return None


def extract_final_response(messages: list) -> str | None:
    """Get the final AI response after tool execution."""

    for message in reversed(messages):
        if (
            getattr(message, "type", None) == "ai"
            and not getattr(message, "tool_calls", [])
        ):
            content = message.content

            if isinstance(content, str):
                return content

            return str(content)

    return None


def evaluate_inventory_case(case: dict, messages: list) -> dict:
    """
    Evaluate tool selection, arguments, and execution outcome
    for one Inventory Agent test case.
    """

    expected_outcome = case["expected_outcome"]

    tool_calls = []
    tool_messages = []

    for message in messages:
        for tool_call in getattr(message, "tool_calls", []):
            tool_calls.append(tool_call)

        if getattr(message, "type", None) == "tool":
            tool_messages.append(message)

    final_response = extract_final_response(messages)

    # Case 1: No tool should be called.
    if expected_outcome == "not_applicable":
        no_tool_called = len(tool_calls) == 0
        response_exists = bool(final_response and final_response.strip())

        checks = {
            "tool_selection": no_tool_called,
            "arguments": no_tool_called,
            "outcome": response_exists,
        }

        return {
            "case_id": case["id"],
            "passed": all(checks.values()),
            "checks": checks,
            "details": (
                "No tool was called, as expected."
                if no_tool_called
                else "Unexpected tool call for an out-of-scope question."
            ),
            "tool_result": None,
            "final_response": final_response,
        }

    # Case 2: A specific tool is expected.
    expected_tool = case["expected_tool"]
    expected_arguments = normalize_arguments(
        case["expected_arguments"]
    )

    matching_calls = [
        call for call in tool_calls
        if call.get("name") == expected_tool
    ]

    if not matching_calls:
        return {
            "case_id": case["id"],
            "passed": False,
            "checks": {
                "tool_selection": False,
                "arguments": False,
                "outcome": False,
            },
            "details": "Expected tool was not called.",
            "tool_result": None,
            "final_response": final_response,
        }

    actual_call = matching_calls[0]

    actual_arguments = normalize_arguments(
        actual_call.get("args", {})
    )

    tool_selection_passed = (
        len(tool_calls) == 1
        and actual_call["name"] == expected_tool
    )

    arguments_passed = (
        actual_arguments == expected_arguments
    )

    matching_messages = [
        message for message in tool_messages
        if getattr(message, "tool_call_id", None)
        == actual_call.get("id")
    ]

    if not matching_messages:
        return {
            "case_id": case["id"],
            "passed": False,
            "checks": {
                "tool_selection": tool_selection_passed,
                "arguments": arguments_passed,
                "outcome": False,
            },
            "details": "Tool was called, but no matching result was found.",
            "tool_result": None,
            "final_response": final_response,
        }

    tool_result = parse_tool_result(
        matching_messages[0].content
    )

    if tool_result is None:
        outcome_passed = False
        details = "Could not parse the tool result."

    elif expected_outcome == "success":
        outcome_passed = tool_result.get("success") is True
        details = "Tool execution outcome checked."

    elif expected_outcome == "error":
        actual_error = tool_result.get("error") or {}
        expected_error = case.get("expected_error_type")

        outcome_passed = (
            tool_result.get("success") is False
            and actual_error.get("type") == expected_error
        )
        details = "Tool error type checked."

    else:
        outcome_passed = False
        details = f"Unsupported expected outcome: {expected_outcome}"

    checks = {
        "tool_selection": tool_selection_passed,
        "arguments": arguments_passed,
        "outcome": outcome_passed,
    }

    return {
        "case_id": case["id"],
        "passed": all(checks.values()),
        "checks": checks,
        "details": details,
        "tool_result": tool_result,
        "final_response": final_response,
    }

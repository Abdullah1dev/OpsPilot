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


def evaluate_inventory_case(case: dict, messages: list) -> dict:
    """
    Evaluate tool selection, arguments, and execution outcome
    for one Inventory Agent test case.
    """

    expected_tool = case["expected_tool"]
    expected_arguments = normalize_arguments(
        case["expected_arguments"]
    )

    tool_calls = []
    tool_messages = []

    for message in messages:
        # AIMessage tool calls
        for tool_call in getattr(message, "tool_calls", []):
            tool_calls.append(tool_call)

        # ToolMessage execution results
        if getattr(message, "type", None) == "tool":
            tool_messages.append(message)

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
                "outcome": False
            },
            "details": "Expected tool was not called."
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
                "outcome": False
            },
            "details": "Tool was called, but no matching result was found."
        }

    tool_result = parse_tool_result(
        matching_messages[0].content
    )

    if tool_result is None:
        outcome_passed = False
        details = "Could not parse the tool result."
    else:
        expected_outcome = case["expected_outcome"]

        if expected_outcome == "success":
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
        "outcome": outcome_passed
    }

    return {
        "case_id": case["id"],
        "passed": all(checks.values()),
        "checks": checks,
        "details": details
    }

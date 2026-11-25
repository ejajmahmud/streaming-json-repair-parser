"""Core incremental JSON auto-closer for partial LLM tool-call streams."""
import json
from typing import Any, List


class StreamingJSONRepair:
    """Repairs and parses incomplete streaming JSON prefixes into valid Python objects."""

    def repair(self, partial: str) -> str:
        s = partial.rstrip()
        if not s:
            return "{}"

        stack: List[str] = []
        in_str = False
        escaped = False

        for ch in s:
            if escaped:
                escaped = False
                continue
            if ch == "\\" and in_str:
                escaped = True
                continue
            if ch == '"':
                in_str = not in_str
                continue
            if not in_str:
                if ch == "{":
                    stack.append("}")
                elif ch == "[":
                    stack.append("]")
                elif ch in ("}", "]") and stack and stack[-1] == ch:
                    stack.pop()

        if escaped:
            s = s[:-1]
        if in_str:
            s += '"'

        s = s.rstrip()
        # Handle dangling colon (e.g. {"key":) by filling null
        if s.endswith(":"):
            s += " null"
        elif s.endswith(","):
            s = s[:-1]

        # If inside an object and last token is a bare string key without colon, drop that incomplete key
        if stack and stack[-1] == "}":
            try:
                json.loads(s + "".join(reversed(stack)))
            except json.JSONDecodeError:
                last_comma = s.rfind(",")
                if last_comma != -1:
                    s = s[:last_comma]

        return s + "".join(reversed(stack))

    def parse_partial(self, partial: str) -> Any:
        repaired = self.repair(partial)
        return json.loads(repaired)

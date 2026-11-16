import ast
import contextlib
import io
import re
from pathlib import Path

README: Path = Path(__file__).parent.parent / "README.md"


class TestReadme:
    def test_usage_prints_what_its_comments_say(self) -> None:
        text: str = README.read_text(encoding="utf-8")
        match: re.Match[str] | None = re.search(r"## Usage\n\n```python\n(.*?)```", text, re.DOTALL)
        assert match is not None
        source: str = match.group(1)
        expected: list[str] = re.findall(r"^print\(.*\)  # (.*)$", source, re.MULTILINE)
        output: io.StringIO = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(compile(ast.parse(source), str(README), "exec"), {})
        assert output.getvalue().splitlines() == expected

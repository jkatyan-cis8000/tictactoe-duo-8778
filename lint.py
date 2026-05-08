"""Linting for source architecture layer enforcement."""

import ast
import sys
from pathlib import Path


LAYERS = ["types_layer", "config", "repo", "service", "runtime", "ui", "providers", "utils"]

# Map each layer to the layers it may import from (forward dependencies)
ALLOWED_IMPORTS = {
    "types_layer": {"types_layer", "self"},
    "config": {"types_layer", "config", "self"},
    "repo": {"types_layer", "config", "repo", "self"},
    "service": {"types_layer", "config", "repo", "providers", "service", "self"},
    "runtime": {"types_layer", "config", "repo", "service", "providers", "runtime", "self"},
    "ui": {"types_layer", "config", "service", "runtime", "providers", "ui", "self"},
    "providers": {"types_layer", "config", "utils", "providers", "self"},
    "utils": {"types_layer", "utils", "self"},
}


def get_layer(filepath: Path) -> str | None:
    """Get the layer directory for a file."""
    parts = filepath.parts
    for i, part in enumerate(parts):
        if part == "src":
            if i + 1 < len(parts):
                return parts[i + 1]
    return None


def get_imports(filepath: Path) -> list[str]:
    """Extract import statements from a Python file."""
    tree = ast.parse(filepath.read_text(), filename=str(filepath))
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level == 0:
                # Absolute import
                if node.module:
                    top = node.module.split(".")[0]
                    imports.append(top)
            elif node.level == 1:
                # Relative import from same layer
                imports.append("self")
            else:
                # Relative import from parent layer - should not happen in our architecture
                imports.append("parent")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                imports.append(top)
    return imports


def check_file(filepath: Path) -> list[str]:
    """Check a single file for linting violations."""
    errors = []

    # Check file length
    lines = filepath.read_text().splitlines()
    if len(lines) > 300:
        errors.append(f"{filepath}: exceeds 300 lines ({len(lines)} lines)")

    # Check layer归属
    layer = get_layer(filepath)
    if layer is None:
        return errors

    # Check imports
    imports = get_imports(filepath)
    allowed = ALLOWED_IMPORTS.get(layer, set())

    for imp in imports:
        # Skip stdlib and third-party imports
        if imp in {"ast", "sys", "os", "typing", "dataclasses", "enum", "pathlib"}:
            continue
        # Skip src imports (cross-layer imports within this project)
        if imp == "src":
            continue
        # Skip self imports (relative imports)
        if imp == "self":
            continue
        # Check if import is allowed
        if imp not in allowed:
            errors.append(
                f"{filepath}: imports '{imp}' which is not in allowed layers {allowed}"
            )

    return errors


def main() -> int:
    """Run linter on all source files."""
    errors: list[str] = []

    src_dir = Path("src")
    if not src_dir.exists():
        print("Error: src/ directory not found")
        return 1

    for filepath in src_dir.rglob("*.py"):
        errors.extend(check_file(filepath))

    if errors:
        print("Linting failed:")
        for err in errors:
            print(f"  {err}")
        return 1

    print("Linting passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

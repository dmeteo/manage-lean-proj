"""Export the FastAPI contract without starting a server."""

import argparse
import json
from pathlib import Path

from app.main import app


def main() -> None:
    parser = argparse.ArgumentParser(description="Export or check the generated OpenAPI schema")
    parser.add_argument("--check", action="store_true", help="fail when openapi.json is out of date")
    args = parser.parse_args()

    target = Path(__file__).resolve().parents[1] / "openapi.json"
    rendered = json.dumps(app.openapi(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != rendered:
            parser.exit(status=1, message=f"OpenAPI is out of date: {target}\n")
        print(f"OpenAPI is up to date: {target}")
    else:
        target.write_text(rendered, encoding="utf-8")
        print(target)


if __name__ == "__main__":
    main()

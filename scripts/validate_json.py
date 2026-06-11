import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PATHS = [
    ROOT / "feature_list.json",
]


def main() -> None:
    for path in PATHS:
        with path.open("r", encoding="utf-8") as handle:
            json.load(handle)
        print(f"valid json: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

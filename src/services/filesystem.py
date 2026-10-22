from pathlib import Path


FILES_ROOT = (Path(__file__).resolve().parents[1] / "resources").resolve()


def _resolve_file(path: str) -> Path:
    candidate = (FILES_ROOT / path).resolve()
    if not candidate.is_relative_to(FILES_ROOT):
        raise ValueError("Path must be inside the configured files root.")
    if not candidate.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    return candidate


def _files() -> list[Path]:
    return sorted(
        (
            path
            for path in FILES_ROOT.rglob("*")
            if path.is_file() and path.resolve().is_relative_to(FILES_ROOT)
        ),
        key=lambda path: path.relative_to(FILES_ROOT).as_posix(),
    )


def list_files() -> list[str]:
    return [path.relative_to(FILES_ROOT).as_posix() for path in _files()]


def search_files(query: str) -> list[str]:
    if not query:
        raise ValueError("Search query must not be empty.")

    matches = []
    for path in _files():
        relative_path = path.relative_to(FILES_ROOT).as_posix()
        if query.casefold() in relative_path.casefold():
            matches.append(relative_path)
            continue

        try:
            if query.casefold() in path.read_text(encoding="utf-8").casefold():
                matches.append(relative_path)
        except UnicodeDecodeError:
            continue

    return sorted(matches)


def read_file(path: str) -> str:
    return _resolve_file(path).read_text(encoding="utf-8")


def file_info(path: str) -> dict[str, str | int]:
    file_path = _resolve_file(path)
    stat = file_path.stat()
    return {
        "path": file_path.relative_to(FILES_ROOT).as_posix(),
        "size": stat.st_size,
        "modified_ns": stat.st_mtime_ns,
    }

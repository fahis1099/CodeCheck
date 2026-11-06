
from pathlib import Path


class FileReader:
    """Responsible for reading Python source files."""

    def read_file(self, file_path):
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not path.is_file():
            raise ValueError("The provided path is not a file.")

        if path.suffix != ".py":
            raise ValueError("Only Python files are supported.")

        return path.read_text(encoding="utf-8")

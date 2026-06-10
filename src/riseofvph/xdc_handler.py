import zipfile
from pathlib import Path


def create_xdc(directory_path: str, output_path: str | None = None) -> str:
    """Create a .xdc file from the contents of a directory.

    Args:
        directory_path: Path to the directory to archive.
        output_path: Desired path for the .xdc file. If not provided,
            the file is created next to the source directory with a .xdc extension.

    Returns:
        The absolute path to the created .xdc file.

    Raises:
        NotADirectoryError: If directory_path is not a directory.
    """
    directory = Path(directory_path)
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory_path}")

    if output_path is None:
        output_path = str(directory.parent / f"{directory.name}.xdc")

    output = Path(output_path)

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(directory.rglob("*")):
            if file_path.is_file():
                arcname = file_path.relative_to(directory)
                zf.write(file_path, arcname)

    return str(output)


def delete_xdc(xdc_path: str) -> None:
    """Delete a .xdc file from disk.

    Args:
        xdc_path: Path to the .xdc file to delete.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(xdc_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {xdc_path}")
    path.unlink()

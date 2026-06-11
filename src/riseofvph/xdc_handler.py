import zipfile
from pathlib import Path


def create_xdc(directory_path: str, output_path: str | None = None) -> str:
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
    path = Path(xdc_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {xdc_path}")
    path.unlink()

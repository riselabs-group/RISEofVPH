import zipfile
from pathlib import Path


def create_xdc(directory_path: Path, output_path: Path | None = None) -> Path:
    directory = Path(directory_path)
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory_path}")

    if output_path is None:
        output_path = directory.parent / f"{directory.name}.xdc"

    output = Path(output_path)

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(directory.rglob("*")):
            if file_path.is_file():
                arcname = file_path.relative_to(directory)
                zf.write(file_path, arcname)

    return output


# TODO:
# Check if the file is a .xdc file
def delete_xdc(xdc_path: Path) -> None:
    if not xdc_path.exists():
        raise FileNotFoundError(f"File not found: {str(xdc_path)}")
    xdc_path.unlink()

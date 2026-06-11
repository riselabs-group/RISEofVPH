import zipfile
import pytest
from pathlib import Path
from src.riseofvph.xdc_handler import create_xdc, delete_xdc



def test_create_xdc_from_directory(tmp_path: Path) -> None:
    """Creating a .xdc from a directory returns the correct path and creates the file."""
    source_dir = tmp_path / "my_extension"
    source_dir.mkdir()
    (source_dir / "file1.txt").write_text("hello")
    (source_dir / "file2.txt").write_text("world")

    result = create_xdc(str(source_dir))

    assert result == str(source_dir.with_suffix(".xdc"))
    assert Path(result).is_file()


def test_create_xdc_produces_valid_zip(tmp_path: Path) -> None:
    """The created .xdc file is a valid zip containing the expected files."""
    source_dir = tmp_path / "ext"
    source_dir.mkdir()
    (source_dir / "data.txt").write_text("content")

    result = create_xdc(str(source_dir))

    with zipfile.ZipFile(result, "r") as zf:
        names = zf.namelist()
        assert "data.txt" in names
        assert zf.read("data.txt").decode() == "content"


def test_create_xdc_with_custom_output_path(tmp_path: Path) -> None:
    """A custom output_path is respected by create_xdc."""
    source_dir = tmp_path / "ext"
    source_dir.mkdir()
    (source_dir / "a.txt").write_text("a")

    custom_output = str(tmp_path / "custom.xdc")
    result = create_xdc(str(source_dir), output_path=custom_output)

    assert result == custom_output
    assert Path(custom_output).is_file()


def test_create_xdc_with_nested_directories(tmp_path: Path) -> None:
    """Nested subdirectories are preserved in the .xdc archive."""
    source_dir = tmp_path / "ext"
    source_dir.mkdir()
    (source_dir / "a.txt").write_text("a")
    nested = source_dir / "subdir"
    nested.mkdir()
    (nested / "b.txt").write_text("b")

    result = create_xdc(str(source_dir))

    with zipfile.ZipFile(result, "r") as zf:
        names = zf.namelist()
        assert "a.txt" in names
        assert "subdir/b.txt" in names


def test_create_xdc_empty_directory(tmp_path: Path) -> None:
    """An empty directory produces a valid (empty) .xdc file."""
    source_dir = tmp_path / "empty_ext"
    source_dir.mkdir()

    result = create_xdc(str(source_dir))

    assert Path(result).is_file()
    with zipfile.ZipFile(result, "r") as zf:
        assert zf.namelist() == []


def test_create_xdc_raises_error_on_file_instead_of_directory(tmp_path: Path) -> None:
    """Passing a file path raises NotADirectoryError."""
    file_path = tmp_path / "not_a_dir.txt"
    file_path.write_text("i am a file")

    with pytest.raises(NotADirectoryError):
        create_xdc(str(file_path))


def test_delete_xdc_removes_file(tmp_path: Path) -> None:
    """delete_xdc removes the .xdc file from disk."""
    xdc_file = tmp_path / "test.xdc"
    xdc_file.write_text("dummy content")

    delete_xdc(str(xdc_file))

    assert not xdc_file.exists()


def test_delete_xdc_raises_error_on_nonexistent_file(tmp_path: Path) -> None:
    """Deleting a file that does not exist raises FileNotFoundError."""
    nonexistent = str(tmp_path / "nonexistent.xdc")

    with pytest.raises(FileNotFoundError):
        delete_xdc(nonexistent)

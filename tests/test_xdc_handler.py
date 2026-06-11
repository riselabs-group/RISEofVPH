import zipfile
import pytest
from pathlib import Path
from src.riseofvph.xdc_handler import create_xdc, delete_xdc

TMP_FILE_NAME = "index.html"
TMP_FILE_CONTENTS = "<p>Hello World!</p>"


def _create_tmp_source_dir(tmp_path: Path) -> Path:
    source_dir = tmp_path / "my_xdc"
    source_dir.mkdir()
    (source_dir / TMP_FILE_NAME).write_text(TMP_FILE_CONTENTS)
    return source_dir


def _at_start(path: Path, custom_output_path=Path("")):
    source_dir = _create_tmp_source_dir(path)
    new_xdc_path = ""

    if custom_output_path == Path(""):
        new_xdc_path = create_xdc(source_dir)
    else:
        new_xdc_path = create_xdc(source_dir, output_path=custom_output_path)

    return source_dir, new_xdc_path


def test_create_xdc_from_directory(tmp_path: Path) -> None:
    source_dir, new_xdc_path = _at_start(tmp_path)

    assert new_xdc_path == source_dir.with_suffix(".xdc")
    assert Path(new_xdc_path).is_file()

def test_create_xdc_with_custom_output_path(tmp_path: Path) -> None:
    source_dir = tmp_path / "ext"
    source_dir.mkdir()
    (source_dir / "a.txt").write_text("a")

    custom_output = str(tmp_path / "custom.xdc")
    result = create_xdc(str(source_dir), output_path=custom_output)

def test_create_xdc_produces_valid_zip(tmp_path: Path) -> None:
    _, new_xdc_path = _at_start(tmp_path)
    assert result == custom_output
    assert Path(custom_output).is_file()

    with zipfile.ZipFile(new_xdc_path, "r") as zf:
        names = zf.namelist()
        assert TMP_FILE_NAME in names
        assert zf.read(TMP_FILE_NAME).decode() == TMP_FILE_CONTENTS

def test_create_xdc_with_nested_directories(tmp_path: Path) -> None:
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
    source_dir = tmp_path / "empty_ext"
    source_dir.mkdir()

    result = create_xdc(str(source_dir))

    assert Path(result).is_file()
    with zipfile.ZipFile(result, "r") as zf:
        assert zf.namelist() == []


def test_create_xdc_raises_error_on_file_instead_of_directory(tmp_path: Path) -> None:
    file_path = tmp_path / "not_a_dir.txt"
    file_path.write_text("i am a file")

    with pytest.raises(NotADirectoryError):
        create_xdc(str(file_path))


def test_delete_xdc_removes_file(tmp_path: Path) -> None:
    xdc_file = tmp_path / "test.xdc"
    xdc_file.write_text("dummy content")

    delete_xdc(str(xdc_file))

    assert not xdc_file.exists()


def test_delete_xdc_raises_error_on_nonexistent_file(tmp_path: Path) -> None:
    nonexistent = str(tmp_path / "nonexistent.xdc")

    with pytest.raises(FileNotFoundError):
        delete_xdc(nonexistent)

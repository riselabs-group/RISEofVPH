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


def test_create_xdc_produces_valid_zip(tmp_path: Path) -> None:
    _, new_xdc_path = _at_start(tmp_path)

    with zipfile.ZipFile(new_xdc_path, "r") as zf:
        names = zf.namelist()
        assert TMP_FILE_NAME in names
        assert zf.read(TMP_FILE_NAME).decode() == TMP_FILE_CONTENTS


def test_create_xdc_with_custom_output_path(tmp_path: Path) -> None:
    custom_dir = tmp_path / "custom.xdc"
    _, new_xdc_path = _at_start(tmp_path, custom_output_path=custom_dir)

    assert new_xdc_path == custom_dir
    assert Path(custom_dir).is_file()


def test_create_xdc_with_nested_directories(tmp_path: Path) -> None:
    source_dir = _create_tmp_source_dir(tmp_path)
    sub_source_dir = _create_tmp_source_dir(source_dir)

    new_xdc_path = create_xdc(source_dir)

    with zipfile.ZipFile(new_xdc_path, "r") as zf:
        names = zf.namelist()
        assert TMP_FILE_NAME in names
        sub_expected_value = sub_source_dir / TMP_FILE_NAME
        clear_sub_expected_value = Path(sub_expected_value).relative_to(source_dir)
        assert str(clear_sub_expected_value) in names


def test_create_xdc_raises_error_on_file_instead_of_directory(tmp_path: Path) -> None:
    file_path = tmp_path / "not_a_dir.txt"
    file_path.write_text("i am a file")

    with pytest.raises(NotADirectoryError):
        create_xdc(file_path)


def test_delete_xdc_file(tmp_path: Path) -> None:
    _, new_xdc_path = _at_start(tmp_path)

    delete_xdc(new_xdc_path)

    assert not new_xdc_path.exists()


def test_delete_xdc_raises_error_on_nonexistent_file(tmp_path: Path) -> None:
    nonexistent_xdc_path = tmp_path / "nonexistent.xdc"

    with pytest.raises(FileNotFoundError):
        delete_xdc(nonexistent_xdc_path)

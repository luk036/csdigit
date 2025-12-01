import pytest
from csdigit.cli import main

__author__ = "Wai-Shing Luk"
__copyright__ = "Wai-Shing Luk"
__license__ = "MIT"


def test_main_to_csd(capsys: pytest.CaptureFixture) -> None:
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["-c", "28.5"])
    captured = capsys.readouterr()
    assert "+00-00.+000" in captured.out


def test_main_to_decimal(capsys: pytest.CaptureFixture) -> None:
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["-d", "+00-00.+000"])
    captured = capsys.readouterr()
    assert "28.5" in captured.out

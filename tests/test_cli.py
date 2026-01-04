import pytest
from csdigit.cli import main, run
from unittest.mock import patch

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


def test_main_to_csdnnz(capsys: pytest.CaptureFixture) -> None:
    """Test CSDNNZ conversion through CLI"""
    main(["-f", "28.5", "-z", "4"])
    captured = capsys.readouterr()
    assert "+00-00.+" in captured.out


def test_main_with_places(capsys: pytest.CaptureFixture) -> None:
    """Test CLI with custom precision"""
    main(["-c", "28.5", "-p", "2"])
    captured = capsys.readouterr()
    assert "+00-00.+0" in captured.out


def test_main_with_verbose(capsys: pytest.CaptureFixture) -> None:
    """Test CLI with verbose logging"""
    main(["-c", "28.5", "-v"])
    captured = capsys.readouterr()
    assert "+00-00.+000" in captured.out
    # Verbose logging is set but may not appear in captured output
    # The important thing is that the command doesn't crash


def test_main_with_debug(capsys: pytest.CaptureFixture) -> None:
    """Test CLI with debug logging"""
    main(["-c", "28.5", "-vv"])
    captured = capsys.readouterr()
    assert "+00-00.+000" in captured.out
    # Debug logging is set but may not appear in captured output
    # The important thing is that the command doesn't crash


def test_main_error_handling(capsys: pytest.CaptureFixture) -> None:
    """Test CLI error handling for invalid input"""
    # Test with invalid CSD string that should trigger error handling
    main(["-d", "+00-00.+X00+"])
    captured = capsys.readouterr()
    # Should still output a result (with logging about unknown character)
    assert captured.out != ""


def test_run_function() -> None:
    """Test the run function that uses sys.argv"""
    with patch("sys.argv", ["csdigit", "-c", "28.5"]):
        # This should not raise an exception
        run()


def test_main_no_arguments(capsys: pytest.CaptureFixture) -> None:
    """Test main with no arguments - should not crash"""
    main([])
    captured = capsys.readouterr()
    # Should not produce any output when no valid arguments provided
    assert captured.out == ""

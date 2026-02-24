import pytest
from decimal import Decimal
from unittest.mock import Mock, patch

from app.calculator_repl import calculator_repl
from app.exceptions import OperationError, ValidationError
import app.calculator_repl as repl_mod


def _printed(mock_print) -> str:
    """Flatten all print() calls into one string for easy contains checks."""
    return "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)


@patch("builtins.print")
@patch("builtins.input", side_effect=["help", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_help_then_exit_saves_history(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    mock_calc_cls.return_value = calc

    calculator_repl()

    out = _printed(mock_print)
    assert "Calculator started. Type 'help' for commands." in out
    assert "Available commands:" in out
    calc.save_history.assert_called_once()
    assert "History saved successfully." in out
    assert "Goodbye!" in out


@patch("builtins.print")
@patch("builtins.input", side_effect=["exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_exit_warns_when_save_history_fails(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    calc.save_history.side_effect = Exception("disk full")
    mock_calc_cls.return_value = calc

    calculator_repl()

    out = _printed(mock_print)
    assert "Warning: Could not save history: disk full" in out
    assert "Goodbye!" in out


@patch("builtins.print")
@patch("builtins.input", side_effect=["history", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_history_empty(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    calc.show_history.return_value = []
    mock_calc_cls.return_value = calc

    calculator_repl()

    out = _printed(mock_print)
    assert "No calculations in history" in out


@patch("builtins.print")
@patch("builtins.input", side_effect=["history", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_history_non_empty_prints_numbered_entries(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    calc.show_history.return_value = ["Addition(2, 3) = 5", "Multiply(4, 5) = 20"]
    mock_calc_cls.return_value = calc

    calculator_repl()

    out = _printed(mock_print)
    assert "Calculation History:" in out
    assert "1. Addition(2, 3) = 5" in out
    assert "2. Multiply(4, 5) = 20" in out


@patch("builtins.print")
@patch("builtins.input", side_effect=["clear", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_clear_history(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    mock_calc_cls.return_value = calc

    calculator_repl()

    calc.clear_history.assert_called_once()
    assert "History cleared" in _printed(mock_print)


@patch("builtins.print")
@patch("builtins.input", side_effect=["undo", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_undo_true(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    calc.undo.return_value = True
    mock_calc_cls.return_value = calc

    calculator_repl()

    assert "Operation undone" in _printed(mock_print)


@patch("builtins.print")
@patch("builtins.input", side_effect=["undo", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_undo_false(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    calc.undo.return_value = False
    mock_calc_cls.return_value = calc

    calculator_repl()

    assert "Nothing to undo" in _printed(mock_print)


@patch("builtins.print")
@patch("builtins.input", side_effect=["redo", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_redo_true(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    calc.redo.return_value = True
    mock_calc_cls.return_value = calc

    calculator_repl()

    assert "Operation redone" in _printed(mock_print)


@patch("builtins.print")
@patch("builtins.input", side_effect=["redo", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_redo_false(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    calc.redo.return_value = False
    mock_calc_cls.return_value = calc

    calculator_repl()

    assert "Nothing to redo" in _printed(mock_print)


@patch("builtins.print")
@patch("builtins.input", side_effect=["save", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_save_success(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    mock_calc_cls.return_value = calc

    calculator_repl()

    calc.save_history.assert_called()
    assert "History saved successfully" in _printed(mock_print)


@patch("builtins.print")
@patch("builtins.input", side_effect=["save", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_save_failure_prints_error(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    calc.save_history.side_effect = Exception("no permission")
    mock_calc_cls.return_value = calc

    calculator_repl()

    out = _printed(mock_print)
    assert "Error saving history: no permission" in out


@patch("builtins.print")
@patch("builtins.input", side_effect=["load", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_load_success(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    mock_calc_cls.return_value = calc

    calculator_repl()

    calc.load_history.assert_called_once()
    assert "History loaded successfully" in _printed(mock_print)


@patch("builtins.print")
@patch("builtins.input", side_effect=["load", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_load_failure_prints_error(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    calc.load_history.side_effect = Exception("corrupt file")
    mock_calc_cls.return_value = calc

    calculator_repl()

    out = _printed(mock_print)
    assert "Error loading history: corrupt file" in out


@patch("builtins.print")
@patch("builtins.input", side_effect=["add", "cancel", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_operation_cancel_on_first_number(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    mock_calc_cls.return_value = calc

    calculator_repl()

    out = _printed(mock_print)
    assert "Operation cancelled" in out
    calc.perform_operation.assert_not_called()


@patch("builtins.print")
@patch("builtins.input", side_effect=["add", "2", "cancel", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_operation_cancel_on_second_number(mock_calc_cls, mock_input, mock_print):
    calc = Mock()
    mock_calc_cls.return_value = calc

    calculator_repl()

    out = _printed(mock_print)
    assert "Operation cancelled" in out
    calc.perform_operation.assert_not_called()


def test_repl_operation_success_runs_decimal_normalize_branch():
    # Fake Decimal class to guarantee isinstance(..., Decimal) is True inside calculator_repl
    class FakeDecimal:
        def __init__(self, value):
            self.value = value
            self.normalize_called = False

        def normalize(self):
            self.normalize_called = True
            return "NORMALIZED"

        def __str__(self):
            return self.value

    calc = Mock()
    op = Mock()

    fake_result = FakeDecimal("5.0")
    calc.perform_operation.return_value = fake_result

    with patch("app.calculator_repl.Calculator", return_value=calc), \
         patch("app.calculator_repl.OperationFactory.create_operation", return_value=op), \
         patch("app.calculator_repl.Decimal", FakeDecimal), \
         patch("builtins.input", side_effect=["add", "2", "3", "exit"]), \
         patch("builtins.print") as mock_print:

        calculator_repl()

    # Prove the branch ran
    assert fake_result.normalize_called is True

    printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)
    assert "Result: NORMALIZED" in printed

def test_repl_decimal_result_takes_normalize_branch():
    calc = Mock()
    op = Mock()

    # Must be a real Decimal instance so isinstance(result, Decimal) is True
    calc.perform_operation.return_value = Decimal("5.0")

    with patch("app.calculator_repl.Calculator", return_value=calc), \
         patch("app.calculator_repl.OperationFactory.create_operation", return_value=op), \
         patch("builtins.input", side_effect=["add", "2", "3", "exit"]), \
         patch("builtins.print") as mock_print:
        calculator_repl()

    # Proves the operation path ran
    calc.set_operation.assert_called_once_with(op)
    calc.perform_operation.assert_called_once_with("2", "3")

    printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)

    # If normalize branch ran, 5.0 becomes 5
    assert "Result: 5" in printed
    assert "Result: 5.0" not in printed

def test_repl_non_decimal_result_skips_normalize_branch():
    calc = Mock()
    op = Mock()

    # Return a NON-Decimal type so isinstance(result, Decimal) is False
    calc.perform_operation.return_value = "5"

    with patch("app.calculator_repl.Calculator", return_value=calc), \
         patch("app.calculator_repl.OperationFactory.create_operation", return_value=op), \
         patch("builtins.input", side_effect=["add", "2", "3", "exit"]), \
         patch("builtins.print") as mock_print:
        calculator_repl()

    printed = "\n".join(str(c.args[0]) for c in mock_print.call_args_list if c.args)

    # It should print the result as-is (no normalize step)
    assert "Result: 5" in printed

@patch("builtins.print")
@patch("app.calculator_repl.OperationFactory.create_operation")
@patch("builtins.input", side_effect=["add", "bad", "3", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_operation_known_error_prints_error_message(
    mock_calc_cls, mock_input, mock_create_operation, mock_print
):
    calc = Mock()
    mock_calc_cls.return_value = calc

    mock_create_operation.return_value = Mock()
    calc.perform_operation.side_effect = ValidationError("Invalid number")

    calculator_repl()

    out = _printed(mock_print)
    assert "Error: Invalid number" in out


@patch("builtins.print")
@patch("app.calculator_repl.OperationFactory.create_operation")
@patch("builtins.input", side_effect=["add", "2", "3", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_operation_unexpected_error_prints_unexpected(
    mock_calc_cls, mock_input, mock_create_operation, mock_print
):
    calc = Mock()
    mock_calc_cls.return_value = calc

    mock_create_operation.return_value = Mock()
    calc.perform_operation.side_effect = Exception("weird")

    calculator_repl()

    out = _printed(mock_print)
    assert "Unexpected error: weird" in out


@patch("builtins.print")
@patch("builtins.input", side_effect=["nonsense", "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_unknown_command(mock_calc_cls, mock_input, mock_print):
    mock_calc_cls.return_value = Mock()

    calculator_repl()

    out = _printed(mock_print)
    assert "Unknown command: 'nonsense'. Type 'help' for available commands." in out


@patch("builtins.print")
@patch("builtins.input", side_effect=[KeyboardInterrupt(), "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_keyboard_interrupt_prints_operation_cancelled(mock_calc_cls, mock_input, mock_print):
    mock_calc_cls.return_value = Mock()

    calculator_repl()

    out = _printed(mock_print)
    assert "Operation cancelled" in out


@patch("builtins.print")
@patch("builtins.input", side_effect=EOFError())
@patch("app.calculator_repl.Calculator")
def test_repl_eoferror_exits_gracefully(mock_calc_cls, mock_input, mock_print):
    mock_calc_cls.return_value = Mock()

    calculator_repl()

    out = _printed(mock_print)
    assert "Input terminated. Exiting..." in out


@patch("builtins.print")
@patch("app.calculator_repl.logging.error")
@patch("app.calculator_repl.Calculator", side_effect=Exception("init boom"))
def test_repl_fatal_init_error_logs_and_raises(mock_calc_cls, mock_log_error, mock_print):
    with pytest.raises(Exception, match="init boom"):
        calculator_repl()

    out = _printed(mock_print)
    assert "Fatal error: init boom" in out
    mock_log_error.assert_called_once()
    assert "Fatal error in calculator REPL: init boom" in mock_log_error.call_args[0][0]


@patch("builtins.print")
@patch("builtins.input", side_effect=[Exception("bad input"), "exit"])
@patch("app.calculator_repl.Calculator")
def test_repl_generic_input_exception_prints_error_and_continues(mock_calc_cls, mock_input, mock_print):
    """
    Covers the generic 'except Exception as e' inside the while-loop.
    """
    mock_calc_cls.return_value = Mock()

    calculator_repl()

    out = _printed(mock_print)
    assert "Error: bad input" in out
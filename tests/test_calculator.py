import datetime
from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import Mock, patch, PropertyMock
from decimal import Decimal
from tempfile import TemporaryDirectory
from app.calculator import Calculator
from app.calculator_repl import calculator_repl
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import LoggingObserver, AutoSaveObserver
from app.operations import OperationFactory

# Fixture to initialize Calculator with a temporary directory for file paths
@pytest.fixture
def calculator():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir=temp_path)

        # Patch properties to use the temporary directory paths
        with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
             patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file, \
             patch.object(CalculatorConfig, 'history_dir', new_callable=PropertyMock) as mock_history_dir, \
             patch.object(CalculatorConfig, 'history_file', new_callable=PropertyMock) as mock_history_file:
            
            # Set return values to use paths within the temporary directory
            mock_log_dir.return_value = temp_path / "logs"
            mock_log_file.return_value = temp_path / "logs/calculator.log"
            mock_history_dir.return_value = temp_path / "history"
            mock_history_file.return_value = temp_path / "history/calculator_history.csv"
            
            # Return an instance of Calculator with the mocked config
            yield Calculator(config=config)

# Test Calculator Initialization

def test_calculator_initialization(calculator):
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    assert calculator.operation_strategy is None

# Test Logging Setup

@patch('app.calculator.logging.info')
def test_logging_setup(logging_info_mock):
    with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
         patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file:
        mock_log_dir.return_value = Path('/tmp/logs')
        mock_log_file.return_value = Path('/tmp/logs/calculator.log')
        
        # Instantiate calculator to trigger logging
        calculator = Calculator(CalculatorConfig())
        logging_info_mock.assert_any_call("Calculator initialized with configuration")

# Test Adding and Removing Observers

def test_add_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    assert observer in calculator.observers

def test_remove_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    calculator.remove_observer(observer)
    assert observer not in calculator.observers

# Test Setting Operations

def test_set_operation(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    assert calculator.operation_strategy == operation

# Test Performing Operations

def test_perform_operation_addition(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    result = calculator.perform_operation(2, 3)
    assert result == Decimal('5')

def test_perform_operation_validation_error(calculator):
    calculator.set_operation(OperationFactory.create_operation('add'))
    with pytest.raises(ValidationError):
        calculator.perform_operation('invalid', 3)

def test_perform_operation_operation_error(calculator):
    with pytest.raises(OperationError, match="No operation set"):
        calculator.perform_operation(2, 3)

# Test Undo/Redo Functionality

def test_undo(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.undo()
    assert calculator.history == []

def test_redo(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.undo()
    calculator.redo()
    assert len(calculator.history) == 1

# Test History Management

@patch('app.calculator.pd.DataFrame.to_csv')
def test_save_history(mock_to_csv, calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.save_history()
    mock_to_csv.assert_called_once()

@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists', return_value=True)
def test_load_history(mock_exists, mock_read_csv, calculator):
    # Mock CSV data to match the expected format in from_dict
    mock_read_csv.return_value = pd.DataFrame({
        'operation': ['Addition'],
        'operand1': ['2'],
        'operand2': ['3'],
        'result': ['5'],
        'timestamp': [datetime.datetime.now().isoformat()]
    })
    
    # Test the load_history functionality
    try:
        calculator.load_history()
        # Verify history length after loading
        assert len(calculator.history) == 1
        # Verify the loaded values
        assert calculator.history[0].operation == "Addition"
        assert calculator.history[0].operand1 == Decimal("2")
        assert calculator.history[0].operand2 == Decimal("3")
        assert calculator.history[0].result == Decimal("5")
    except OperationError:
        pytest.fail("Loading history failed due to OperationError")
        
            
# Test Clearing History

def test_clear_history(calculator):
    operation = OperationFactory.create_operation('add')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 3)
    calculator.clear_history()
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []

# Test REPL Commands (using patches for input/output handling)

@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        calculator_repl()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call("History saved successfully.")
        mock_print.assert_any_call("Goodbye!")

@patch('builtins.input', side_effect=['help', 'exit'])
@patch('builtins.print')
def test_calculator_repl_help(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nAvailable commands:")

@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
def test_calculator_repl_addition(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nResult: 5")

# Added Test Coverage

@patch("app.calculator.logging.warning")
@patch.object(Calculator, "load_history", side_effect=Exception("boom"))
def test_init_logs_warning_when_load_history_fails(mock_load_history, mock_warning):
    
    Calculator()

    mock_warning.assert_called_once()
    assert "Could not load existing history: boom" in mock_warning.call_args[0][0]

@patch("app.calculator.print")
@patch("app.calculator.logging.basicConfig", side_effect=Exception("config failure"))
def test_setup_logging_exception(mock_basicconfig, mock_print):
    with pytest.raises(Exception, match="config failure"):
        Calculator()

    # Assert: print was called with the error message
    mock_print.assert_called_once()
    mock_print.assert_any_call("Error setting up logging: config failure")

@patch("app.calculator.logging.error")
@patch("app.calculator.InputValidator.validate_number", side_effect=Exception("boom"))
def test_perform_operation_wraps_generic_exception_as_operationerror(
    mock_validate_number, mock_logging_error, calculator
):
    """
    Covers perform_operation() generic exception handler:
    logging.error("Operation failed: ...")
    raise OperationError("Operation failed: ...")
    """
    calculator.set_operation(OperationFactory.create_operation("add"))

    with pytest.raises(OperationError, match=r"Operation failed: boom"):
        calculator.perform_operation(2, 3)

    mock_logging_error.assert_called_once()
    assert "Operation failed: boom" in mock_logging_error.call_args[0][0]

def test_perform_operation_operation_error(calculator):
    with pytest.raises(OperationError, match="No operation set"):
        calculator.perform_operation(2, 3)

def test_history_trimmed_when_exceeds_max_size(calculator):
    calculator.config.max_history_size = 1
    calculator.set_operation(OperationFactory.create_operation('add'))

    calculator.perform_operation(2, 3)  # first calc
    calculator.perform_operation(5, 6)  # second calc -> should trigger pop(0)

    assert len(calculator.history) == 1
    # The remaining history entry should be the most recent one
    last = calculator.history[0]
    assert last.operand1 == Decimal("5")
    assert last.operand2 == Decimal("6")
    assert last.operation == "Addition"

def test_perform_operation_exception(calculator):
    calculator.set_operation(OperationFactory.create_operation('add'))
    with pytest.raises(Exception):
        calculator.perform_operation('invalid', 3)

@patch("app.calculator.pd.DataFrame.to_csv")
def test_save_history_empty_history_writes_headers_csv(mock_to_csv, calculator):
    """
    Covers save_history() branch when history_data is empty.
    """
    calculator.history = []  # ensure empty

    calculator.save_history()

    mock_to_csv.assert_called_once()
    assert mock_to_csv.call_args.kwargs.get("index") is False


@patch("app.calculator.pd.DataFrame.to_csv", side_effect=Exception("write failed"))
def test_save_history_raises_operationerror_on_failure(mock_to_csv, calculator):
    """
    Covers save_history() exception -> OperationError.
    """
    calculator.history = []  # forces empty-history branch, still calls to_csv

    with pytest.raises(OperationError, match="Failed to save history: write failed"):
        calculator.save_history()


@patch("app.calculator.pd.read_csv")
@patch("app.calculator.Path.exists", return_value=True)
def test_load_history_file_exists_but_empty_df(mock_exists, mock_read_csv, calculator):
    """
    Covers load_history() branch when CSV exists but DataFrame is empty.
    """
    mock_read_csv.return_value = pd.DataFrame()  # empty df

    calculator.load_history()

    assert calculator.history == []


@patch("app.calculator.Path.exists", return_value=False)
def test_load_history_file_missing_starts_empty(mock_exists, calculator):
    """
    Covers load_history() branch when history file does not exist.
    """
    calculator.load_history()
    assert calculator.history == []


@patch("app.calculator.pd.read_csv", side_effect=Exception("bad csv"))
@patch("app.calculator.Path.exists", return_value=True)
def test_load_history_raises_operationerror_on_failure(mock_exists, mock_read_csv, calculator):
    """
    Covers load_history() exception -> OperationError.
    """
    with pytest.raises(OperationError, match="Failed to load history: bad csv"):
        calculator.load_history()


def test_get_history_dataframe_has_expected_columns_and_values(calculator):
    """
    Covers get_history_dataframe().
    """
    calculator.set_operation(OperationFactory.create_operation("add"))
    calculator.perform_operation(2, 3)

    df = calculator.get_history_dataframe()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert set(["operation", "operand1", "operand2", "result", "timestamp"]).issubset(df.columns)

    assert df.loc[0, "operation"] == "Addition"
    assert str(df.loc[0, "operand1"]) == "2"
    assert str(df.loc[0, "operand2"]) == "3"
    assert str(df.loc[0, "result"]) == "5"


def test_show_history_formats_output_strings(calculator):
    """
    Covers show_history().
    """
    calculator.set_operation(OperationFactory.create_operation("add"))
    calculator.perform_operation(2, 3)

    lines = calculator.show_history()

    assert lines == ["Addition(2, 3) = 5"]


@patch("app.calculator.logging.info")
def test_clear_history_clears_history_and_stacks_and_logs(mock_log_info, calculator):
    """
    Covers clear_history() and its log line.
    """
    calculator.set_operation(OperationFactory.create_operation("add"))
    calculator.perform_operation(2, 3)

    assert len(calculator.history) == 1
    assert len(calculator.undo_stack) == 1

    calculator.clear_history()

    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    mock_log_info.assert_any_call("History cleared")


def test_undo_returns_false_when_stack_empty(calculator):
    """
    Covers undo() early return when undo_stack is empty.
    """
    calculator.undo_stack = []
    assert calculator.undo() is False


def test_redo_returns_false_when_stack_empty(calculator):
    """
    Covers redo() early return when redo_stack is empty.
    """
    calculator.redo_stack = []
    assert calculator.redo() is False
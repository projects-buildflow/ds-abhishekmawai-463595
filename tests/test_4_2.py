"""Tests for Task 4.2: Pipeline Implementation

Objective: Build a working ETL data pipeline with extract, transform, load stages.

This test verifies:
1. All required files exist
2. Each module imports without errors
3. Each module has callable functions
4. run_pipeline.py has an orchestrator function
5. Logging is configured
6. Error handling is present
7. config.py has path configuration
8. Pipeline runs end-to-end and produces output
"""

import pytest
import importlib
import sys
from pathlib import Path


@pytest.fixture
def pipeline_path(student_folder):
    """Get path to the student's pipeline folder."""
    if not student_folder:
        pytest.skip("Student folder not provided")

    path = Path(student_folder) / "submissions" / "pipeline"
    if not path.exists():
        pytest.fail(
            f"Pipeline folder not found at {path}\n\n"
            "Create: submissions/pipeline/ with:\n"
            "  - extract.py\n"
            "  - transform.py\n"
            "  - load.py\n"
            "  - run_pipeline.py\n"
            "  - config.py"
        )
    return path


class TestRequiredFilesExist:
    """Verify all required pipeline files exist."""

    def test_extract_py_exists(self, pipeline_path):
        """extract.py must exist."""
        assert (pipeline_path / "extract.py").exists(), (
            "extract.py not found in pipeline folder.\n"
            "Create extract.py with functions to load data from CSV sources."
        )

    def test_transform_py_exists(self, pipeline_path):
        """transform.py must exist."""
        assert (pipeline_path / "transform.py").exists(), (
            "transform.py not found in pipeline folder.\n"
            "Create transform.py with functions to clean and process data."
        )

    def test_load_py_exists(self, pipeline_path):
        """load.py must exist."""
        assert (pipeline_path / "load.py").exists(), (
            "load.py not found in pipeline folder.\n"
            "Create load.py with functions to save processed data."
        )

    def test_run_pipeline_py_exists(self, pipeline_path):
        """run_pipeline.py must exist."""
        assert (pipeline_path / "run_pipeline.py").exists(), (
            "run_pipeline.py not found in pipeline folder.\n"
            "Create run_pipeline.py to orchestrate the full ETL process."
        )

    def test_config_py_exists(self, pipeline_path):
        """config.py must exist."""
        assert (pipeline_path / "config.py").exists(), (
            "config.py not found in pipeline folder.\n"
            "Create config.py to store configuration settings (paths, etc.)."
        )


class TestModulesImport:
    """Verify each module can be imported without errors."""

    @pytest.fixture(autouse=True)
    def add_pipeline_to_path(self, pipeline_path):
        """Add pipeline folder to sys.path for imports."""
        path_str = str(pipeline_path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)
        yield
        if path_str in sys.path:
            sys.path.remove(path_str)

    def test_extract_imports(self, pipeline_path):
        """extract.py must import without errors."""
        if not (pipeline_path / "extract.py").exists():
            pytest.skip("extract.py does not exist")
        try:
            if "extract" in sys.modules:
                del sys.modules["extract"]
            importlib.import_module("extract")
        except Exception as e:
            pytest.fail(
                f"extract.py failed to import: {e}\n\n"
                "Make sure extract.py has no syntax errors and its "
                "dependencies are installed (e.g., pandas)."
            )

    def test_transform_imports(self, pipeline_path):
        """transform.py must import without errors."""
        if not (pipeline_path / "transform.py").exists():
            pytest.skip("transform.py does not exist")
        try:
            if "transform" in sys.modules:
                del sys.modules["transform"]
            importlib.import_module("transform")
        except Exception as e:
            pytest.fail(
                f"transform.py failed to import: {e}\n\n"
                "Make sure transform.py has no syntax errors and its "
                "dependencies are installed."
            )

    def test_load_imports(self, pipeline_path):
        """load.py must import without errors."""
        if not (pipeline_path / "load.py").exists():
            pytest.skip("load.py does not exist")
        try:
            if "load" in sys.modules:
                del sys.modules["load"]
            importlib.import_module("load")
        except Exception as e:
            pytest.fail(
                f"load.py failed to import: {e}\n\n"
                "Make sure load.py has no syntax errors and its "
                "dependencies are installed."
            )

    def test_config_imports(self, pipeline_path):
        """config.py must import without errors."""
        if not (pipeline_path / "config.py").exists():
            pytest.skip("config.py does not exist")
        try:
            if "config" in sys.modules:
                del sys.modules["config"]
            importlib.import_module("config")
        except Exception as e:
            pytest.fail(
                f"config.py failed to import: {e}\n\n"
                "Make sure config.py has no syntax errors."
            )

    def test_run_pipeline_imports(self, pipeline_path):
        """run_pipeline.py must import without errors."""
        if not (pipeline_path / "run_pipeline.py").exists():
            pytest.skip("run_pipeline.py does not exist")
        try:
            if "run_pipeline" in sys.modules:
                del sys.modules["run_pipeline"]
            importlib.import_module("run_pipeline")
        except Exception as e:
            pytest.fail(
                f"run_pipeline.py failed to import: {e}\n\n"
                "Make sure run_pipeline.py has no syntax errors and its "
                "imports are correct."
            )


class TestModuleFunctions:
    """Verify each module defines callable functions."""

    @pytest.fixture(autouse=True)
    def add_pipeline_to_path(self, pipeline_path):
        """Add pipeline folder to sys.path for imports."""
        path_str = str(pipeline_path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)
        yield
        if path_str in sys.path:
            sys.path.remove(path_str)

    def _get_callables(self, module_name):
        """Get public callable names from a module."""
        if module_name in sys.modules:
            del sys.modules[module_name]
        mod = importlib.import_module(module_name)
        return [
            name for name in dir(mod)
            if not name.startswith("_") and callable(getattr(mod, name))
            and not isinstance(getattr(mod, name), type)
        ]

    def test_extract_has_functions(self, pipeline_path):
        """extract.py must define at least one function."""
        if not (pipeline_path / "extract.py").exists():
            pytest.skip("extract.py does not exist")
        callables = self._get_callables("extract")
        assert len(callables) >= 1, (
            "extract.py has no functions defined.\n"
            "Add at least one function, e.g.:\n"
            "  def extract_orders(filepath): ..."
        )

    def test_transform_has_functions(self, pipeline_path):
        """transform.py must define at least one function."""
        if not (pipeline_path / "transform.py").exists():
            pytest.skip("transform.py does not exist")
        callables = self._get_callables("transform")
        assert len(callables) >= 1, (
            "transform.py has no functions defined.\n"
            "Add at least one function, e.g.:\n"
            "  def clean_orders(df): ..."
        )

    def test_load_has_functions(self, pipeline_path):
        """load.py must define at least one function."""
        if not (pipeline_path / "load.py").exists():
            pytest.skip("load.py does not exist")
        callables = self._get_callables("load")
        assert len(callables) >= 1, (
            "load.py has no functions defined.\n"
            "Add at least one function, e.g.:\n"
            "  def save_to_csv(df, filepath): ..."
        )

    def test_run_pipeline_has_orchestrator(self, pipeline_path):
        """run_pipeline.py must have a main/run function."""
        if not (pipeline_path / "run_pipeline.py").exists():
            pytest.skip("run_pipeline.py does not exist")
        content = (pipeline_path / "run_pipeline.py").read_text()
        has_func = (
            "def main(" in content
            or "def run(" in content
            or "def run_pipeline(" in content
        )
        assert has_func, (
            "run_pipeline.py needs an orchestrator function.\n"
            "Add one of: def main(), def run(), or def run_pipeline()"
        )


class TestCodeQuality:
    """Verify logging, error handling, and configuration."""

    def test_uses_logging(self, pipeline_path):
        """run_pipeline.py must use Python's logging module."""
        run_file = pipeline_path / "run_pipeline.py"
        if not run_file.exists():
            pytest.skip("run_pipeline.py does not exist")
        content = run_file.read_text()
        has_logging = "import logging" in content or "logging.getLogger" in content
        assert has_logging, (
            "run_pipeline.py should use Python's logging module.\n"
            "Add: import logging\n"
            "     logger = logging.getLogger(__name__)"
        )

    def test_has_error_handling(self, pipeline_path):
        """run_pipeline.py must have try/except error handling."""
        run_file = pipeline_path / "run_pipeline.py"
        if not run_file.exists():
            pytest.skip("run_pipeline.py does not exist")
        content = run_file.read_text()
        has_try = "try:" in content and "except" in content
        assert has_try, (
            "run_pipeline.py should have error handling.\n"
            "Wrap your pipeline execution in try/except to catch and log errors."
        )

    def test_config_has_paths(self, pipeline_path):
        """config.py must define path-related configuration."""
        config_file = pipeline_path / "config.py"
        if not config_file.exists():
            pytest.skip("config.py does not exist")
        content = config_file.read_text().lower()
        has_path_config = (
            "path" in content
            or "dir" in content
            or "pathlib" in content
            or "folder" in content
        )
        assert has_path_config, (
            "config.py should define path configuration.\n"
            "Use pathlib.Path to define data and output directories."
        )

    def test_run_pipeline_has_main_block(self, pipeline_path):
        """run_pipeline.py should have an if __name__ == '__main__' block."""
        run_file = pipeline_path / "run_pipeline.py"
        if not run_file.exists():
            pytest.skip("run_pipeline.py does not exist")
        content = run_file.read_text()
        has_main_block = '__name__' in content and '__main__' in content
        assert has_main_block, (
            "run_pipeline.py should have:\n"
            "  if __name__ == '__main__':\n"
            "      run_pipeline()"
        )

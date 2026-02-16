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
8. Pipeline runs end-to-end with sample data
9. Pipeline produces output files
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


class TestPipelineExecution:
    """Run the pipeline end-to-end with sample data and verify output."""

    SAMPLE_ORDERS = (
        "order_id,customer_id,order_date,product,quantity,unit_price,status\n"
        "1,101,2024-01-15,Widget A,2,29.99,completed\n"
        "2,102,2024-01-15,Widget B,1,49.99,completed\n"
        "3,101,2024-01-16,Widget A,3,29.99,completed\n"
        "4,103,2024-01-16,Widget C,1,19.99,cancelled\n"
        "5,102,2024-01-17,Widget B,2,49.99,pending\n"
    )

    SAMPLE_CUSTOMERS = (
        "customer_id,name,email,signup_date,region\n"
        "101,Alice Smith,alice@example.com,2023-06-01,North\n"
        "102,Bob Jones,bob@example.com,2023-07-15,South\n"
        "103,Carol Lee,carol@example.com,2023-08-20,North\n"
    )

    @pytest.fixture
    def setup_sample_data(self, pipeline_path):
        """Create sample CSV files so the pipeline has data to process."""
        # Look for data/ relative to repo root (4 levels up from submissions/pipeline/)
        repo_root = pipeline_path.parent.parent
        data_dir = repo_root / "data"
        data_dir.mkdir(exist_ok=True)

        orders_file = data_dir / "orders.csv"
        customers_file = data_dir / "customers.csv"

        # Only create if missing — don't overwrite existing data
        created = []
        if not orders_file.exists():
            orders_file.write_text(self.SAMPLE_ORDERS)
            created.append(orders_file)
        if not customers_file.exists():
            customers_file.write_text(self.SAMPLE_CUSTOMERS)
            created.append(customers_file)

        yield data_dir

        # Clean up only files we created
        for f in created:
            if f.exists():
                f.unlink()

    @pytest.fixture(autouse=True)
    def add_pipeline_to_path(self, pipeline_path):
        """Add pipeline folder to sys.path for imports."""
        path_str = str(pipeline_path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)
        yield
        if path_str in sys.path:
            sys.path.remove(path_str)

    def _find_orchestrator(self):
        """Import run_pipeline and find the orchestrator function."""
        if "run_pipeline" in sys.modules:
            del sys.modules["run_pipeline"]
        mod = importlib.import_module("run_pipeline")
        for name in ["run_pipeline", "main", "run"]:
            fn = getattr(mod, name, None)
            if fn and callable(fn):
                return fn
        return None

    def test_pipeline_runs_without_error(self, pipeline_path, setup_sample_data):
        """Pipeline must execute without raising an exception."""
        for req in ["extract.py", "transform.py", "load.py", "run_pipeline.py", "config.py"]:
            if not (pipeline_path / req).exists():
                pytest.skip(f"{req} does not exist")

        fn = self._find_orchestrator()
        if fn is None:
            pytest.skip("No orchestrator function found")

        import os
        old_cwd = os.getcwd()
        try:
            os.chdir(str(pipeline_path))
            fn()
        except Exception as e:
            pytest.fail(
                f"Pipeline crashed during execution: {e}\n\n"
                "Your pipeline should handle errors gracefully.\n"
                "Make sure it can process the sample data without crashing."
            )
        finally:
            os.chdir(old_cwd)

    def test_pipeline_produces_output(self, pipeline_path, setup_sample_data):
        """Pipeline must create at least one output file."""
        for req in ["extract.py", "transform.py", "load.py", "run_pipeline.py", "config.py"]:
            if not (pipeline_path / req).exists():
                pytest.skip(f"{req} does not exist")

        fn = self._find_orchestrator()
        if fn is None:
            pytest.skip("No orchestrator function found")

        # Collect existing files before running
        def get_all_files(root):
            return set(str(p) for p in root.rglob("*") if p.is_file())

        repo_root = pipeline_path.parent.parent
        files_before = get_all_files(repo_root)

        import os
        old_cwd = os.getcwd()
        try:
            os.chdir(str(pipeline_path))
            fn()
        except Exception:
            pytest.skip("Pipeline crashed — see test_pipeline_runs_without_error")
        finally:
            os.chdir(old_cwd)

        files_after = get_all_files(repo_root)
        new_files = files_after - files_before

        # Filter to likely output files (csv, json, txt, parquet)
        output_extensions = {".csv", ".json", ".txt", ".parquet", ".xlsx"}
        output_files = [
            f for f in new_files
            if Path(f).suffix.lower() in output_extensions
        ]

        assert len(output_files) >= 1, (
            "Pipeline ran but did not produce any output files.\n"
            "Your load stage should save results (e.g., CSV files) "
            "to an output directory."
        )

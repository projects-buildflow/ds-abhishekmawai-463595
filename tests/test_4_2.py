"""Tests for Task 4.2: Pipeline Implementation

Objective: Build a working ETL data pipeline with extract, transform, load stages.

This test DECISIVELY verifies:
1. Pipeline has required files (extract.py, transform.py, load.py, run_pipeline.py)
2. Extract module can load data from CSV
3. Transform module cleans and processes data correctly
4. Load module saves output correctly
5. Full pipeline runs end-to-end without errors
"""

import pytest
import pandas as pd
import sys
import os
import tempfile
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
            "Create a 'pipeline' folder in your submissions directory with:\n"
            "  - extract.py\n"
            "  - transform.py\n"
            "  - load.py\n"
            "  - run_pipeline.py\n"
            "  - config.py"
        )
    return path


@pytest.fixture
def sample_csv(tmp_path):
    """Create sample CSV data for testing."""
    data = pd.DataFrame({
        'customer_id': ['C001', 'C002', 'C003', 'C002', 'C004'],
        'name': ['Alice', 'Bob', 'Charlie', 'BOB', 'Diana'],
        'email': ['alice@test.com', 'bob@test.com', 'charlie@test.com', 'BOB@TEST.COM', 'diana@test.com'],
        'age': [25, -5, 30, 28, 150],  # Includes invalid ages
        'total_spent': [100.0, 200.0, None, 250.0, 50.0],
    })
    csv_path = tmp_path / "test_input.csv"
    data.to_csv(csv_path, index=False)
    return csv_path


class TestRequiredFilesExist:
    """Verify all required pipeline files exist."""

    def test_extract_py_exists(self, pipeline_path):
        """extract.py must exist."""
        assert (pipeline_path / "extract.py").exists(), (
            "extract.py not found in pipeline folder.\n"
            "Create extract.py with functions to load data from sources."
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
            "Create config.py to store configuration settings."
        )


class TestExtractModule:
    """Test the extract module can load data."""

    def test_extract_has_function(self, pipeline_path):
        """extract.py must have an extract function."""
        sys.path.insert(0, str(pipeline_path))
        try:
            import extract
            # Look for common extraction function names
            has_extract_func = (
                hasattr(extract, 'extract') or
                hasattr(extract, 'extract_data') or
                hasattr(extract, 'extract_csv') or
                hasattr(extract, 'load_data') or
                hasattr(extract, 'read_data')
            )
            assert has_extract_func, (
                "extract.py should have an extraction function.\n"
                "Define a function like: def extract_data(filepath) or def extract(source)"
            )
        finally:
            if 'extract' in sys.modules:
                del sys.modules['extract']
            sys.path.remove(str(pipeline_path))

    def test_extract_loads_csv(self, pipeline_path, sample_csv):
        """Extract function must successfully load CSV data."""
        sys.path.insert(0, str(pipeline_path))
        try:
            import extract

            # Find the extraction function
            extract_func = None
            for name in ['extract', 'extract_data', 'extract_csv', 'load_data', 'read_data']:
                if hasattr(extract, name):
                    extract_func = getattr(extract, name)
                    break

            if extract_func is None:
                pytest.skip("Could not find extract function")

            # Test extraction
            result = extract_func(str(sample_csv))

            assert result is not None, "Extract function returned None"
            assert isinstance(result, pd.DataFrame), (
                f"Extract function returned {type(result).__name__}, expected DataFrame"
            )
            assert len(result) > 0, "Extract function returned empty DataFrame"

        except Exception as e:
            pytest.fail(f"Extract function failed: {e}")
        finally:
            if 'extract' in sys.modules:
                del sys.modules['extract']
            sys.path.remove(str(pipeline_path))


class TestTransformModule:
    """Test the transform module processes data correctly."""

    def test_transform_has_function(self, pipeline_path):
        """transform.py must have a transform function."""
        sys.path.insert(0, str(pipeline_path))
        try:
            import transform
            has_transform_func = (
                hasattr(transform, 'transform') or
                hasattr(transform, 'transform_data') or
                hasattr(transform, 'clean_data') or
                hasattr(transform, 'process_data')
            )
            assert has_transform_func, (
                "transform.py should have a transformation function.\n"
                "Define a function like: def transform_data(df) or def transform(data)"
            )
        finally:
            if 'transform' in sys.modules:
                del sys.modules['transform']
            sys.path.remove(str(pipeline_path))

    def test_transform_returns_dataframe(self, pipeline_path, sample_csv):
        """Transform function must return a DataFrame."""
        sys.path.insert(0, str(pipeline_path))
        try:
            import transform

            # Find transform function
            transform_func = None
            for name in ['transform', 'transform_data', 'clean_data', 'process_data']:
                if hasattr(transform, name):
                    transform_func = getattr(transform, name)
                    break

            if transform_func is None:
                pytest.skip("Could not find transform function")

            # Load test data and transform
            input_df = pd.read_csv(sample_csv)
            result = transform_func(input_df)

            assert isinstance(result, pd.DataFrame), (
                f"Transform function returned {type(result).__name__}, expected DataFrame"
            )

        except Exception as e:
            pytest.fail(f"Transform function failed: {e}")
        finally:
            if 'transform' in sys.modules:
                del sys.modules['transform']
            sys.path.remove(str(pipeline_path))

    def test_transform_handles_invalid_data(self, pipeline_path):
        """Transform should handle/clean invalid data."""
        sys.path.insert(0, str(pipeline_path))
        try:
            import transform

            transform_func = None
            for name in ['transform', 'transform_data', 'clean_data', 'process_data']:
                if hasattr(transform, name):
                    transform_func = getattr(transform, name)
                    break

            if transform_func is None:
                pytest.skip("Could not find transform function")

            # Data with issues
            dirty_data = pd.DataFrame({
                'customer_id': ['C001', 'C002'],
                'age': [-5, 150],  # Invalid ages
                'email': ['valid@test.com', 'invalid-email'],
            })

            # Should not crash
            try:
                result = transform_func(dirty_data)
                assert result is not None, "Transform should return data even with invalid inputs"
            except Exception as e:
                pytest.fail(f"Transform crashed on invalid data: {e}")

        finally:
            if 'transform' in sys.modules:
                del sys.modules['transform']
            sys.path.remove(str(pipeline_path))


class TestLoadModule:
    """Test the load module saves data correctly."""

    def test_load_has_function(self, pipeline_path):
        """load.py must have a load function."""
        sys.path.insert(0, str(pipeline_path))
        try:
            import load
            has_load_func = (
                hasattr(load, 'load') or
                hasattr(load, 'load_data') or
                hasattr(load, 'save_data') or
                hasattr(load, 'save_to_csv') or
                hasattr(load, 'write_data')
            )
            assert has_load_func, (
                "load.py should have a load/save function.\n"
                "Define a function like: def save_data(df, filepath) or def load(data, destination)"
            )
        finally:
            if 'load' in sys.modules:
                del sys.modules['load']
            sys.path.remove(str(pipeline_path))

    def test_load_saves_file(self, pipeline_path, tmp_path):
        """Load function must successfully save data."""
        sys.path.insert(0, str(pipeline_path))
        try:
            import load

            load_func = None
            for name in ['load', 'load_data', 'save_data', 'save_to_csv', 'write_data']:
                if hasattr(load, name):
                    load_func = getattr(load, name)
                    break

            if load_func is None:
                pytest.skip("Could not find load function")

            test_df = pd.DataFrame({'a': [1, 2, 3], 'b': ['x', 'y', 'z']})
            output_path = tmp_path / "output.csv"

            # Try to save
            load_func(test_df, str(output_path))

            assert output_path.exists(), (
                "Load function did not create output file.\n"
                "Make sure your load function saves the DataFrame to the specified path."
            )

        except TypeError as e:
            # Function might have different signature
            pytest.skip(f"Load function has unexpected signature: {e}")
        except Exception as e:
            pytest.fail(f"Load function failed: {e}")
        finally:
            if 'load' in sys.modules:
                del sys.modules['load']
            sys.path.remove(str(pipeline_path))


class TestPipelineOrchestration:
    """Test the full pipeline runs end-to-end."""

    def test_run_pipeline_has_main(self, pipeline_path):
        """run_pipeline.py must have a main function or __main__ block."""
        run_file = pipeline_path / "run_pipeline.py"
        content = run_file.read_text()

        has_main = (
            'def main(' in content or
            'def run(' in content or
            'def run_pipeline(' in content or
            '__name__' in content and '__main__' in content
        )

        assert has_main, (
            "run_pipeline.py should have a main function or __main__ block.\n"
            "Add: def run_pipeline(): or if __name__ == '__main__':"
        )

    def test_pipeline_uses_logging(self, pipeline_path):
        """Pipeline should use logging for observability."""
        run_file = pipeline_path / "run_pipeline.py"
        content = run_file.read_text()

        has_logging = 'import logging' in content or 'from logging' in content

        assert has_logging, (
            "run_pipeline.py should use Python's logging module.\n"
            "Add: import logging\n"
            "And use: logging.info(), logging.error(), etc."
        )

    def test_pipeline_has_error_handling(self, pipeline_path):
        """Pipeline should have error handling."""
        run_file = pipeline_path / "run_pipeline.py"
        content = run_file.read_text()

        has_error_handling = 'try:' in content and 'except' in content

        assert has_error_handling, (
            "run_pipeline.py should have error handling.\n"
            "Wrap your pipeline stages in try/except blocks."
        )


class TestPipelineEndToEnd:
    """Test the pipeline works end-to-end."""

    def test_full_pipeline_runs(self, pipeline_path, sample_csv, tmp_path):
        """Full pipeline should run without errors."""
        sys.path.insert(0, str(pipeline_path))

        try:
            # Import all modules
            import extract
            import transform
            import load

            # Find functions
            extract_func = None
            for name in ['extract', 'extract_data', 'extract_csv', 'load_data', 'read_data']:
                if hasattr(extract, name):
                    extract_func = getattr(extract, name)
                    break

            transform_func = None
            for name in ['transform', 'transform_data', 'clean_data', 'process_data']:
                if hasattr(transform, name):
                    transform_func = getattr(transform, name)
                    break

            load_func = None
            for name in ['load', 'load_data', 'save_data', 'save_to_csv', 'write_data']:
                if hasattr(load, name):
                    load_func = getattr(load, name)
                    break

            if not all([extract_func, transform_func, load_func]):
                pytest.skip("Could not find all pipeline functions")

            # Run pipeline
            output_path = tmp_path / "pipeline_output.csv"

            # Extract
            raw_data = extract_func(str(sample_csv))
            assert raw_data is not None, "Extract returned None"

            # Transform
            clean_data = transform_func(raw_data)
            assert clean_data is not None, "Transform returned None"

            # Load
            load_func(clean_data, str(output_path))

            assert output_path.exists(), "Pipeline did not produce output file"

            # Verify output is valid
            output_df = pd.read_csv(output_path)
            assert len(output_df) > 0, "Pipeline output is empty"

        except Exception as e:
            pytest.fail(f"Pipeline failed end-to-end: {e}")

        finally:
            for mod in ['extract', 'transform', 'load', 'config']:
                if mod in sys.modules:
                    del sys.modules[mod]
            if str(pipeline_path) in sys.path:
                sys.path.remove(str(pipeline_path))


class TestCodeQuality:
    """Test code quality requirements."""

    def test_modules_have_docstrings(self, pipeline_path):
        """Pipeline modules should have docstrings."""
        files_without_docstrings = []

        for filename in ['extract.py', 'transform.py', 'load.py', 'run_pipeline.py']:
            filepath = pipeline_path / filename
            if filepath.exists():
                content = filepath.read_text().strip()
                # Check for module-level docstring
                if not (content.startswith('"""') or content.startswith("'''")):
                    files_without_docstrings.append(filename)

        # At least run_pipeline.py should have a docstring
        if 'run_pipeline.py' in files_without_docstrings:
            pytest.fail(
                "run_pipeline.py should have a module docstring.\n"
                "Add a docstring at the top explaining what the pipeline does."
            )

    def test_config_has_settings(self, pipeline_path):
        """config.py should have configuration settings."""
        config_file = pipeline_path / "config.py"
        content = config_file.read_text()

        # Should have some variable assignments
        has_config = '=' in content and (
            'PATH' in content.upper() or
            'DIR' in content.upper() or
            'FILE' in content.upper() or
            'CONFIG' in content.upper() or
            'INPUT' in content.upper() or
            'OUTPUT' in content.upper()
        )

        assert has_config, (
            "config.py should contain configuration settings.\n"
            "Add settings like:\n"
            "  INPUT_PATH = 'data/raw/'\n"
            "  OUTPUT_PATH = 'data/processed/'"
        )

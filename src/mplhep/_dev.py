"""
Development helper script for mplhep. Vibe-coded.

Usage: ./dev [command] [options] or ./dev for interactive mode
"""

from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import questionary
    from questionary import Style

    HAS_QUESTIONARY = True
except ImportError:
    questionary = None  # type: ignore[assignment]
    Style = None  # type: ignore[assignment]
    HAS_QUESTIONARY = False


def check_dev_dependencies() -> bool:
    """Check if questionary is available."""
    if HAS_QUESTIONARY:
        return True

    print("\n🔧 Missing development dependencies (questionary)")
    print('📦 Install with: python -m pip install --upgrade --editable ".[all]"')
    return False


class DevScript:
    """Main development script class."""

    def __init__(self):
        self.default_jobs = self._get_default_jobs()
        self.project_root = Path.cwd()
        self.style = self._get_style()

    def _get_default_jobs(self) -> int:
        """Get default number of parallel jobs (half of CPU cores)."""
        try:
            cpu_count = os.cpu_count() or 4
            return max(1, cpu_count // 2)
        except (TypeError, AttributeError):
            return 4

    def _print_header(self, text: str) -> None:
        """Print a formatted header."""
        print(f"\n🔵 === {text} ===")

    def _print_success(self, text: str) -> None:
        """Print a success message."""
        print(f"  ✅ {text}")

    def _print_warning(self, text: str) -> None:
        """Print a warning message."""
        print(f"  ⚠️ {text}")

    def _print_error(self, text: str) -> None:
        """Print an error message."""
        print(f"  ❌ {text}")

    def _get_terminal_width(self) -> int:
        """Get terminal width, fallback to 80 if unavailable."""
        try:
            return shutil.get_terminal_size().columns
        except (AttributeError, OSError):
            return 80

    def _run_command_with_confirmation(
        self, cmd: list[str], prompt: str = "Confirm command (editable):"
    ) -> bool:
        """Run a command with user confirmation and editing capability."""
        if not HAS_QUESTIONARY or questionary is None:
            return self._run_command(cmd)

        modified_cmd_str = questionary.text(
            prompt, default=" ".join(cmd), style=self.style
        ).ask()

        if modified_cmd_str is None:
            return False

        if modified_cmd_str.strip():
            try:
                cmd = shlex.split(modified_cmd_str)
            except ValueError as e:
                self._print_error(f"Invalid command syntax: {e}")
                return False

        return self._run_command(cmd)

    def _run_command(self, cmd: list[str], cwd: Path | None = None) -> bool:
        """Run a command and return True if successful."""
        self._print_header(f"Running: {' '.join(cmd)}")
        separator = 3 * ("=" * self._get_terminal_width() + "\n")
        print(separator)

        try:
            result = subprocess.run(cmd, cwd=cwd or self.project_root, check=True)
        except subprocess.CalledProcessError as e:
            self._print_error(f"Command failed with exit code {e.returncode}")
            return False
        except FileNotFoundError:
            self._print_error(f"Command not found: {cmd[0]}")
            return False

        print(separator)
        return result.returncode == 0

    def _show_summary(self, items: list[Path], title: str) -> None:
        """Show a formatted summary of items."""
        if not items:
            return

        print(f"\n📋 {title}:")
        for item in items[:10]:  # Show first 10 items
            item_type = "📁" if item.is_dir() else "📄"
            print(f"  {item_type} {item.relative_to(self.project_root)}")

        if len(items) > 10:
            print(f"  ... and {len(items) - 10} more items")

    def _confirm(self, message: str, default: bool = False) -> bool:
        """Ask for confirmation using questionary."""
        if not HAS_QUESTIONARY or questionary is None:
            response = (
                input(f"{message} [{'Y/n' if default else 'y/N'}]: ").strip().lower()
            )
            if default:
                return response in ["", "y", "yes"]
            return response in ["y", "yes"]

        return questionary.confirm(
            message, default=default, style=self._get_style()
        ).ask()

    def _find_files_to_clean(self) -> list[Path]:
        """Find files and directories that can be cleaned."""
        items_to_clean = []

        # Standard cleanup targets
        cleanup_targets = [
            "pytest_results",
            "__pycache__",
            ".pytest_cache",
            ".coverage",
            ".mypy_cache",
            "htmlcov",
            "dist",
            "build",
            "*.egg-info",
        ]

        for target in cleanup_targets:
            if "*" in target:
                # Handle glob patterns
                items_to_clean.extend(self.project_root.glob(target))
            else:
                item = self.project_root / target
                if item.exists():
                    items_to_clean.append(item)

        # Find all __pycache__ directories recursively
        for pycache in self.project_root.rglob("__pycache__"):
            if pycache not in items_to_clean:
                items_to_clean.append(pycache)

        return items_to_clean

    def cmd_test(
        self,
        jobs: int | None = None,
        filter_pattern: str | None = None,
        skip_cleanup: bool = False,
        extra_args: list[str] | None = None,
    ) -> bool:
        """Run pytest with matplotlib comparison."""
        if jobs is None:
            jobs = self.default_jobs

        # Handle pytest_results cleanup (only for direct command-line usage)
        if not skip_cleanup:
            self._handle_pytest_results_cleanup()

        self._print_header("Running Tests")

        # Build pytest command
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "-r",
            "sa",
            "--mpl",
            "--mpl-results-path=pytest_results",
        ]

        # Only add -n flag if using parallelism (jobs > 1)
        if jobs > 1:
            cmd.extend(["-n", str(jobs)])

        if filter_pattern:
            cmd.extend(["-k", filter_pattern])

        # Add any extra arguments passed through from CLI
        if extra_args:
            cmd.extend(extra_args)

        success = self._run_command_with_confirmation(cmd)

        if success:
            self._print_success("Tests completed successfully!")
        else:
            self._print_error("Tests failed!")

        return success

    def cmd_baseline(self) -> bool:
        """Generate baseline images for matplotlib comparison tests."""
        self._print_header("Generating Baseline Images")

        # Ask for baseline directory path
        baseline_path = self._get_text_input(
            "Confirm baseline path:",
            default="tests/baseline",
            fallback_prompt="Enter baseline directory path",
        )

        if baseline_path is None:
            self._print_warning("Baseline generation cancelled")
            return False

        if not baseline_path.strip():
            baseline_path = "tests/baseline"
            self._print_warning("Empty path provided, using default: tests/baseline")

        # Check if directory exists and warn about overwriting
        baseline_dir = Path(baseline_path)
        if baseline_dir.exists() and any(baseline_dir.iterdir()):
            self._print_warning(
                f"Directory '{baseline_path}' exists and contains files!"
            )
            self._print_warning("Existing baseline images will be overwritten.")
            if not self._confirm("Continue with baseline generation?", default=True):
                self._print_warning("Baseline generation cancelled")
                return False
        else:
            self._print_success(f"Will generate baselines in: {baseline_path}")

        # Build baseline generation command based on CONTRIBUTING.md
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "-r",
            "sa",
            "--mpl",
            "-n",
            str(self.default_jobs),
            f"--mpl-generate-path={baseline_path}",
        ]

        success = self._run_command_with_confirmation(cmd)

        if success:
            self._print_success("Baseline generation completed successfully!")
            self._print_warning(
                "Only include actually modified baseline images in your PR!"
            )
            self._print_warning("Review generated baselines before committing.")
        else:
            self._print_error("Baseline generation failed!")

        return success

    def cmd_precommit(self, extra_args: list[str] | None = None) -> bool:
        """Run pre-commit hooks on all files."""
        self._print_header("Running Pre-commit Hooks")

        # Check if pre-commit is available
        if not self._check_tool_available("prek", ["prek", "--version"]):
            return False

        cmd = ["prek", "run", "--all-files"]

        # Add any extra arguments
        if extra_args:
            cmd.extend(extra_args)

        success = self._run_command_with_confirmation(cmd)

        if success:
            self._print_success("Pre-commit hooks completed successfully!")
        else:
            self._print_error("Pre-commit hooks failed!")

        return success
        """Clean up test artifacts and cache files."""
        self._print_header("Cleaning Test Artifacts")

        items_to_clean = self._find_files_to_clean()

        if not items_to_clean:
            self._print_success("Nothing to clean!")
            return True

        self._show_summary(
            items_to_clean, f"Items to be removed ({len(items_to_clean)} total)"
        )

        if not self._confirm(
            f"Remove these {len(items_to_clean)} items?", default=True
        ):
            self._print_warning("Clean operation cancelled")
            return True

        removed_count = 0
        for item in items_to_clean:
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                removed_count += 1
                if len(items_to_clean) <= 10:  # Show individual items for small lists
                    self._print_success(
                        f"Removed {item.relative_to(self.project_root)}"
                    )
            except OSError as e:  # noqa: PERF203
                self._print_error(f"Failed to remove {item}: {e}")

        if len(items_to_clean) > 10:
            self._print_success(
                f"Successfully removed {removed_count}/{len(items_to_clean)} items"
            )

        return True

    def cmd_docs(
        self,
        action: str = "build",
        port: int = 8000,
        clean: bool = True,
        fast: bool = False,
        extra_args: list[str] | None = None,
    ) -> bool:
        """Build or serve documentation."""
        # Check if mkdocs is available
        if not self._check_tool_available("mkdocs", ["mkdocs", "--version"]):
            return False

        # Check if new_docs directory exists
        docs_dir = self.project_root / "new_docs"
        if not docs_dir.exists():
            self._print_error("new_docs directory not found!")
            return False

        if action == "build":
            return self._build_docs(clean, fast, extra_args)
        if action == "serve":
            return self._serve_docs(port, fast, extra_args)
        self._print_error(f"Unknown docs action: {action}")
        return False

    def _build_docs(
        self, clean: bool, fast: bool, extra_args: list[str] | None = None
    ) -> bool:
        """Build documentation."""
        if fast:
            self._print_header("Building Documentation (FAST MODE - no figures)")
            self._print_warning("⚡ Figure rendering disabled for faster builds")
        else:
            self._print_header("Building Documentation")

        cmd = ["mkdocs", "build"]

        # Use fast config if requested
        if fast:
            cmd.extend(["-f", "mkdocs_norender.yml"])

        if clean:
            cmd.append("--clean")

        # Add any extra arguments
        if extra_args:
            cmd.extend(extra_args)

        success = self._run_command(cmd, cwd=self.project_root / "new_docs")

        if success:
            if fast:
                self._print_success("Fast documentation build completed!")
                self._print_warning("Note: Figures were not rendered")
            else:
                self._print_success("Documentation built successfully!")
            site_dir = self.project_root / "new_docs" / "site"
            if site_dir.exists():
                self._print_success(f"Built site available at: {site_dir}")
        else:
            self._print_error("Documentation build failed!")

        return success

    def _serve_docs(
        self, port: int, fast: bool, extra_args: list[str] | None = None
    ) -> bool:
        """Serve documentation locally."""
        if fast:
            self._print_header(
                f"Serving Documentation on port {port} (FAST MODE - no figures)"
            )
            self._print_warning("⚡ Figure rendering disabled for faster builds")
        else:
            self._print_header(f"Serving Documentation on port {port}")

        cmd = ["mkdocs", "serve", "--dev-addr", f"127.0.0.1:{port}"]

        # Use fast config if requested
        if fast:
            cmd.extend(["-f", "mkdocs_norender.yml"])

        # Add any extra arguments
        if extra_args:
            cmd.extend(extra_args)

        self._print_success(
            f"Documentation will be available at: http://127.0.0.1:{port}"
        )
        if fast:
            self._print_warning(
                "⚡ Fast mode: Builds ~50x faster but figures not rendered"
            )
        self._print_warning("Press Ctrl+C to stop the server")

        # For serve, we don't use confirmation since it's a long-running process
        return self._run_command(cmd, cwd=self.project_root / "new_docs")

    def cmd_clean(self) -> bool:
        """Clean up test artifacts and cache files."""
        self._print_header("Cleaning Test Artifacts")

        items_to_clean = self._find_files_to_clean()

        if not items_to_clean:
            self._print_success("Nothing to clean!")
            return True

        self._show_summary(
            items_to_clean, f"Items to be removed ({len(items_to_clean)} total)"
        )

        if not self._confirm(
            f"Remove these {len(items_to_clean)} items?", default=True
        ):
            self._print_warning("Clean operation cancelled")
            return True

        removed_count = 0
        for item in items_to_clean:
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                removed_count += 1
                if len(items_to_clean) <= 10:  # Show individual items for small lists
                    self._print_success(
                        f"Removed {item.relative_to(self.project_root)}"
                    )
            except OSError as e:  # noqa: PERF203
                self._print_error(f"Failed to remove {item}: {e}")

        if len(items_to_clean) > 10:
            self._print_success(
                f"Successfully removed {removed_count}/{len(items_to_clean)} items"
            )

        return True

    def cmd_benchmark(
        self,
        action: str = "run",
        baseline_name: str | None = None,
        compare_with: str | None = None,
    ) -> bool:
        """Run performance benchmarks."""
        # Check if pytest-benchmark is available
        if not self._check_benchmark_available():
            return False

        self._print_header(f"Benchmark {action.title()}")

        # Ensure benchmark baseline directory exists
        benchmark_dir = self.project_root / "tests" / "baseline" / "benchmark"
        benchmark_dir.mkdir(parents=True, exist_ok=True)

        if action == "run":
            return self._run_benchmarks(baseline_name)
        if action == "compare":
            return self._compare_benchmarks(compare_with)
        if action == "list":
            return self._list_benchmarks()
        if action == "clean":
            return self._clean_benchmarks()
        self._print_error(f"Unknown benchmark action: {action}")
        return False

    def _check_benchmark_available(self) -> bool:
        """Check if pytest-benchmark is available."""
        if importlib.util.find_spec("pytest_benchmark") is not None:
            self._print_success("pytest-benchmark is available")
            return True
        self._print_error("pytest-benchmark not found!")
        self._print_warning("Install with: pip install pytest-benchmark")
        return False

    def _run_benchmarks(self, baseline_name: str | None = None) -> bool:
        """Run benchmark tests."""
        # Build benchmark command
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "--benchmark-only",  # Only run benchmark tests
            "--benchmark-sort=mean",  # Sort by mean execution time
            "--benchmark-warmup=on",  # Enable warmup rounds
        ]

        # Configure benchmark storage
        benchmark_dir = self.project_root / "tests" / "baseline" / "benchmark"
        cmd.extend([f"--benchmark-storage={benchmark_dir}"])

        if baseline_name:
            cmd.append(f"--benchmark-save={baseline_name}")
            self._print_success(f"Will save benchmark results as: {baseline_name}")
        else:
            # Auto-generate baseline name with timestamp
            timestamp = datetime.datetime.now(tz=datetime.timezone.utc).strftime(
                "%Y%m%d_%H%M%S"
            )
            baseline_name = f"run_{timestamp}"
            cmd.append(f"--benchmark-save={baseline_name}")
            self._print_success(f"Will save benchmark results as: {baseline_name}")

        success = self._run_command_with_confirmation(cmd)

        if success:
            self._print_success("Benchmarks completed successfully!")
            self._print_success(f"Results saved as: {baseline_name}")
            self._print_warning(
                "Use './dev benchmark compare --with <baseline>' to compare results"
            )
        else:
            self._print_error("Benchmarks failed!")

        return success

    def _compare_benchmarks(self, compare_with: str | None = None) -> bool:
        """Compare current benchmarks with a baseline."""
        benchmark_dir = self.project_root / "tests" / "baseline" / "benchmark"

        if not compare_with:
            # List available benchmark files for selection
            available_files = self._get_available_benchmark_files()
            if not available_files:
                self._print_error("No benchmark files found!")
                self._print_warning("Run './dev benchmark run --save <name>' first")
                return False

            if HAS_QUESTIONARY and questionary is not None:
                compare_with = questionary.select(
                    "Select baseline to compare with:",
                    choices=available_files,
                    style=self.style,
                ).ask()
                if not compare_with:
                    self._print_warning("Comparison cancelled")
                    return False
            else:
                self._print_warning("Available benchmark files:")
                for i, baseline in enumerate(available_files, 1):
                    print(f"  {i}. {baseline}")
                try:
                    choice = int(input("Enter choice number: ")) - 1
                    compare_with = available_files[choice]
                except (ValueError, IndexError):
                    self._print_error("Invalid choice")
                    return False

        # Build comparison command
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "--benchmark-only",
            "--benchmark-sort=mean",
            f"--benchmark-storage={benchmark_dir}",
            f"--benchmark-compare={compare_with}",
        ]

        success = self._run_command_with_confirmation(cmd)

        if success:
            self._print_success("Benchmark comparison completed!")
        else:
            self._print_warning("Benchmark comparison found performance differences")
            self._print_warning("Review the output above for details")

        return (
            True  # Return True even for performance regressions as it's informational
        )

    def _list_benchmarks(self) -> bool:
        """List available benchmark baselines."""
        benchmark_dir = self.project_root / "tests" / "baseline" / "benchmark"

        if not benchmark_dir.exists():
            self._print_warning("No benchmark directory found")
            return True

        available_baselines = self._get_available_baselines()

        if not available_baselines:
            self._print_warning("No benchmark baselines found")
            self._print_warning(
                "Run './dev benchmark run --save <name>' to create baselines"
            )
        else:
            self._print_success(
                f"Found {len(available_baselines)} benchmark baseline(s):"
            )
            for baseline in available_baselines:
                baseline_path = benchmark_dir / baseline
                if baseline_path.exists():
                    # Try to get more info about the baseline
                    try:
                        json_files = list(baseline_path.glob("*.json"))
                        if json_files:
                            with open(json_files[0]) as f:
                                data = json.load(f)
                                timestamp = data.get("datetime", "Unknown time")
                                commit_info = data.get("commit_info", {})
                                commit_id = (
                                    commit_info.get("id", "Unknown")[:8]
                                    if commit_info.get("id")
                                    else "Unknown"
                                )
                                print(
                                    f"  📊 {baseline} (commit: {commit_id}, {timestamp})"
                                )
                        else:
                            print(f"  📊 {baseline}")
                    except (json.JSONDecodeError, FileNotFoundError, KeyError):
                        print(f"  📊 {baseline}")
                else:
                    print(f"  📊 {baseline} (missing data)")

        return True

    def _clean_benchmarks(self) -> bool:
        """Clean up benchmark results."""
        benchmark_dir = self.project_root / "tests" / "baseline" / "benchmark"

        if not benchmark_dir.exists() or not any(benchmark_dir.iterdir()):
            self._print_success("No benchmark data to clean!")
            return True

        # Get list of benchmark baselines
        available_baselines = self._get_available_baselines()

        if not available_baselines:
            # Clean up empty directory structure
            try:
                benchmark_dir.rmdir()
                self._print_success("Removed empty benchmark directory")
            except OSError:
                pass
            return True

        self._print_warning(f"Found {len(available_baselines)} benchmark baseline(s)")
        for baseline in available_baselines:
            print(f"  📊 {baseline}")

        if not self._confirm("Remove all benchmark baselines?", default=False):
            self._print_warning("Benchmark cleanup cancelled")
            return True

        # Remove all benchmark data
        try:
            shutil.rmtree(benchmark_dir)
            self._print_success("All benchmark data removed!")
        except OSError as e:
            self._print_error(f"Failed to remove benchmark data: {e}")
            return False

        return True

    def _get_available_baselines(self) -> list[str]:
        """Get list of available benchmark baselines."""
        benchmark_dir = self.project_root / "tests" / "baseline" / "benchmark"

        if not benchmark_dir.exists():
            return []

        baselines = [
            item.name
            for item in benchmark_dir.iterdir()
            if item.is_dir() and not item.name.startswith(".")
        ]

        return sorted(baselines)

    def _get_available_benchmark_files(self) -> list[str]:
        """Get list of available benchmark JSON files for comparison."""
        benchmark_dir = self.project_root / "tests" / "baseline" / "benchmark"

        if not benchmark_dir.exists():
            return []

        benchmark_files = [
            json_file.stem
            for subdir in benchmark_dir.iterdir()
            if subdir.is_dir() and not subdir.name.startswith(".")
            for json_file in subdir.glob("*.json")
        ]

        return sorted(benchmark_files)

    def show_help(self) -> None:
        """Show help information."""
        help_text = f"""
🚀 mplhep Development Helper

Usage:
  ./dev                    Interactive mode (menu)
  ./dev <command> [opts]   Direct command mode

Commands:
  test      Run pytest with matplotlib comparison
  baseline  Generate baseline images for matplotlib tests
  benchmark Run performance benchmarks
  docs      Build or serve documentation
  clean     Clean up test artifacts
  precommit Run pre-commit hooks on all files
  help      Show this help

Test command options:
  -n, --jobs N     Number of parallel jobs (default: {self.default_jobs})
  -k, --filter     Run only tests matching pattern
  --skip-cleanup   Keep existing pytest_results directory
  [pytest args]    Any unrecognized arguments are passed through to pytest

Benchmark command options:
  run              Run benchmarks and save results
  compare          Compare with previous benchmark results
  list             List available benchmark baselines
  clean            Remove all benchmark data
  --save NAME      Save benchmark results with custom name
  --with NAME      Compare with specific baseline

Docs command options:
  build            Build documentation (default action)
  serve            Serve documentation locally
  --port PORT      Port for serve command (default: 8000)
  --no-clean       Skip --clean flag for build command
  --fast           Fast mode: disable figure rendering (~50x faster builds)

Examples:
  ./dev test -n 4                      # Run tests with 4 jobs
  ./dev test -k "test_basic"           # Run only tests matching "test_basic"
  ./dev test --verbose -s              # Pass pytest arguments directly
  ./dev benchmark run --save baseline  # Run benchmarks and save as 'baseline'
  ./dev benchmark compare --with baseline  # Compare with 'baseline'
  ./dev benchmark list                 # List available baselines
  ./dev docs build                     # Build documentation (full with figures)
  ./dev docs build --fast              # Fast build without figures (~3s vs ~160s)
  ./dev docs serve --fast              # Serve with fast rebuilds on changes
  ./dev docs serve --port 8080         # Serve documentation on port 8080
  ./dev clean                          # Clean up test artifacts
        """
        print(help_text)

    def _get_style(self):
        """Get questionary style."""
        if not HAS_QUESTIONARY or Style is None:
            return None

        return Style(
            [
                ("qmark", ""),  # Remove question mark
                ("question", "bold"),
                ("answer", "fg:#ff9d00 bold"),
                ("pointer", "fg:#ff9d00 bold"),
                ("highlighted", "fg:#ff9d00 bold"),
                ("selected", "fg:#cc5454"),
                ("separator", "fg:#cc5454"),
                ("instruction", ""),
                ("text", ""),
                ("disabled", "fg:#858585 italic"),
            ]
        )

    def _get_text_input(
        self, prompt: str, default: str = "", fallback_prompt: str = ""
    ) -> str | None:
        """Get text input with questionary or basic fallback."""
        if HAS_QUESTIONARY and questionary is not None:
            return questionary.text(prompt, default=default, style=self.style).ask()
        # Fallback mode
        display_prompt = fallback_prompt or prompt
        if default:
            display_prompt += f" [{default}]"
        display_prompt += ": "

        response = input(display_prompt).strip()
        return response if response else default

    def _get_choice(
        self, prompt: str, choices: list[tuple], fallback_prompt: str = ""
    ) -> str | None:
        """Get choice selection with questionary or basic fallback."""
        if HAS_QUESTIONARY and questionary is not None:
            choice_objects = [
                questionary.Choice(label, value) for label, value in choices
            ]
            return questionary.select(
                prompt, choices=choice_objects, style=self.style
            ).ask()
        # Fallback mode
        print(f"\n{fallback_prompt or prompt}")
        for i, (label, _) in enumerate(choices, 1):
            print(f"  {i}. {label}")

        try:
            while True:
                response = input("Enter choice (number): ").strip()
                idx = int(response) - 1
                if 0 <= idx < len(choices):
                    return choices[idx][1]
                print(f"Please enter a number between 1 and {len(choices)}")
        except (ValueError, KeyboardInterrupt):
            return None

    def _check_tool_available(self, tool_name: str, check_cmd: list[str]) -> bool:
        """Check if a tool is available."""
        try:
            result = subprocess.run(
                check_cmd, capture_output=True, text=True, check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            self._print_error(f"{tool_name} not found!")
            self._print_warning(f"Please install {tool_name} to use this feature")
            return False

        self._print_success(f"{tool_name} version: {result.stdout.strip()}")
        return True

    def _handle_pytest_results_cleanup(self) -> None:
        """Handle cleanup of pytest_results directory."""
        pytest_results = self.project_root / "pytest_results"
        if pytest_results.exists():
            if self._confirm(
                "Remove existing pytest_results/ directory?", default=True
            ):
                self._print_warning("Removing existing pytest_results/ directory...")
                shutil.rmtree(pytest_results)
                self._print_success("Removed pytest_results/")
            else:
                self._print_warning("Keeping existing pytest_results/")

    def _get_test_modules(self) -> list[str]:
        """Get available test modules/directories."""
        test_modules = []

        # Look for tests directory
        tests_dir = self.project_root / "tests"
        if tests_dir.exists() and tests_dir.is_dir():
            # Find Python test files and directories
            for item in tests_dir.iterdir():
                if (
                    item.is_file()
                    and item.name.startswith("test_")
                    and item.suffix == ".py"
                ):
                    # Remove .py extension and add to list
                    module_name = item.stem
                    test_modules.append(module_name)
                elif (
                    item.is_dir()
                    and not item.name.startswith(".")
                    and item.name != "__pycache__"
                ):
                    # Check if directory contains test files
                    if any(
                        f.name.startswith("test_") and f.suffix == ".py"
                        for f in item.iterdir()
                        if f.is_file()
                    ):
                        test_modules.append(item.name)

        # Also look for test files in src directory structure
        src_dir = self.project_root / "src"
        if src_dir.exists():
            for test_file in src_dir.rglob("test_*.py"):
                relative_path = test_file.relative_to(src_dir)
                module_path = str(relative_path.with_suffix("")).replace("/", ".")
                if module_path not in test_modules:
                    test_modules.append(module_path)

        return sorted(test_modules)

    def _interactive_test_options(self) -> dict:
        """Get test options interactively."""
        print("\n🔧 Configure Test Run")

        # Jobs selection with choices
        jobs_choices = [
            (f"🚀 Default ({self.default_jobs} cores)", "default"),
            ("🔄 No parallelism", "none"),
            ("⚙️ Custom number", "custom"),
        ]

        jobs_choice = self._get_choice(
            "Parallel execution mode:", jobs_choices, "Select parallel execution mode:"
        )

        if jobs_choice == "default":
            jobs = self.default_jobs
        elif jobs_choice == "none":
            jobs = 1
        elif jobs_choice == "custom":
            jobs_input = self._get_text_input(
                "Enter number of parallel jobs:",
                default=str(self.default_jobs),
                fallback_prompt="Enter number of parallel jobs",
            )
            if jobs_input is None:
                jobs = self.default_jobs
                self._print_warning(f"Input cancelled, using default: {jobs}")
            else:
                try:
                    jobs = int(jobs_input)
                    jobs = max(1, jobs)  # Ensure at least 1
                except (ValueError, TypeError):
                    jobs = self.default_jobs
                    self._print_warning(f"Invalid jobs value, using default: {jobs}")
        else:
            jobs = self.default_jobs

        # Test selection with choices
        test_choices = [
            ("🎯 Run all tests", "all"),
            ("📦 Select submodules", "submodules"),
            ("🔍 Custom pattern", "custom"),
        ]

        test_choice = self._get_choice(
            "Test selection mode:", test_choices, "Select test mode:"
        )

        filter_pattern = None
        if test_choice == "all":
            filter_pattern = None
        elif test_choice == "submodules":
            # Get available test modules/directories
            test_modules = self._get_test_modules()
            if test_modules:
                while True:
                    selected_modules = questionary.checkbox(
                        "Select test modules to run:",
                        choices=[
                            questionary.Choice(module, module)
                            for module in test_modules
                        ],
                        style=self._get_style(),
                    ).ask()

                    if selected_modules:
                        # Display selected modules
                        print(f"\n📦 Selected modules: {', '.join(selected_modules)}")
                        # Convert selected modules to pytest pattern
                        filter_pattern = f"'{' or '.join(selected_modules)}'"
                        print(f"🔍 Pattern: {filter_pattern}")
                        break
                    self._print_warning("No modules selected!")
                    retry = questionary.confirm(
                        "Use <space> to select, <enter> to confirm. Otherwise, run all tests.",
                        default=True,
                        style=self._get_style(),
                    ).ask()

                    if not retry:
                        self._print_warning("Running all tests instead")
                        filter_pattern = None
                        break
            else:
                self._print_warning("No test modules found, running all tests")
                filter_pattern = None
        elif test_choice == "custom":
            print("\n💡 Custom pattern examples:")
            examples = [
                "test_basic                    - Run tests matching 'test_basic'",
                "test_plot                     - Run tests matching 'test_plot'",
                "test_basic or test_plot       - Run tests matching either pattern",
                "test_basic and not slow       - Run test_basic but exclude 'slow' tests",
                "TestClass                     - Run all tests in TestClass",
                "TestClass::test_method        - Run specific test method",
                "test_*.py                     - Run tests in files matching pattern",
            ]
            for example in examples:
                print(f"  • {example}")

            filter_pattern = self._get_text_input(
                "Enter custom test pattern:",
                fallback_prompt="Enter custom test pattern",
            )
            if not filter_pattern or not filter_pattern.strip():
                self._print_warning("No pattern entered - all tests will be run")
                filter_pattern = None

        return {
            "jobs": jobs,
            "filter_pattern": filter_pattern,
        }

    def _print_interactive_header(self) -> None:
        """Print the interactive mode header."""
        print("\n" + "=" * 60)
        print("🚀 mplhep Development Helper - Interactive Mode")
        print("=" * 60)

    def interactive_mode(self) -> None:
        """Run in interactive mode with questionary menu."""
        if not HAS_QUESTIONARY or questionary is None:
            print("\n❌ Interactive mode requires questionary.")
            print('Install with: python -m pip install --upgrade --editable ".[all]"')
            print("\nFallback: Use direct commands like './dev test' or './dev help'")
            return

        # self._print_interactive_header()

        # Create styled menu choices with colored command snippets
        def make_menu_item(title, command_text):
            return f"{title}\n       └─ {command_text}"

        menu_choices = [
            (
                make_menu_item("🔍 Run pre-commit", "prek run --all-files"),
                "precommit",
            ),
            (
                make_menu_item(
                    "🧪 Run pytest",
                    "python -m pytest -r sa --mpl --mpl-results-path=pytest_results",
                ),
                "test",
            ),
            (
                make_menu_item(
                    "🖼️ Run pytest (generate new baseline)",
                    "python -m pytest -r sa --mpl --mpl-generate-path=tests/baseline",
                ),
                "baseline",
            ),
            (
                make_menu_item(
                    "📚 Build documentation", "cd new_docs && mkdocs build --clean"
                ),
                "docs_build",
            ),
            (
                make_menu_item(
                    "⚡ Build documentation (fast)",
                    "cd new_docs && mkdocs build -f mkdocs_norender.yml",
                ),
                "docs_build_fast",
            ),
            (
                make_menu_item("🌐 Serve documentation", "cd new_docs && mkdocs serve"),
                "docs_serve",
            ),
            (
                make_menu_item(
                    "⚡ Serve documentation (fast)",
                    "cd new_docs && mkdocs serve -f mkdocs_norender.yml",
                ),
                "docs_serve_fast",
            ),
            (
                make_menu_item(
                    "⚡ Run benchmarks", "python -m pytest --benchmark-only"
                ),
                "benchmark",
            ),
            (
                make_menu_item(
                    "🧹 Remove Artifacts", "rm -rf __pycache__ pytest_results .coverage"
                ),
                "clean",
            ),
            (
                make_menu_item("📖 Help", "Show detailed help and usage examples"),
                "help",
            ),
            ("🚪 Exit", "exit"),
        ]

        while True:
            try:
                self._print_interactive_header()
                choice = self._get_choice(
                    "What would you like to do?",
                    menu_choices,
                    "Main Menu - What would you like to do?",
                )

                if choice is None or choice == "exit":
                    print("\n👋 Goodbye!")
                    break
                if choice == "test":
                    # Handle pytest_results cleanup first
                    self._handle_pytest_results_cleanup()
                    options = self._interactive_test_options()
                    self.cmd_test(**options, skip_cleanup=True, extra_args=None)
                elif choice == "baseline":
                    self.cmd_baseline()
                elif choice == "clean":
                    self.cmd_clean()
                elif choice == "precommit":
                    self.cmd_precommit()
                elif choice == "docs_build":
                    self.cmd_docs("build", clean=True, fast=False)
                elif choice == "docs_build_fast":
                    self.cmd_docs("build", clean=True, fast=True)
                elif choice == "docs_serve":
                    self.cmd_docs("serve", port=8000, fast=False)
                elif choice == "docs_serve_fast":
                    self.cmd_docs("serve", port=8000, fast=True)
                elif choice == "benchmark":
                    self._interactive_benchmark_menu()
                elif choice == "help":
                    self.show_help()

                # Continue to main menu (no additional prompt needed)

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

    def _interactive_benchmark_menu(self) -> None:
        """Interactive benchmark menu."""
        if not self._check_benchmark_available():
            return

        benchmark_choices = [
            ("⚡ Run benchmarks", "run"),
            ("📊 Compare with baseline", "compare"),
            ("📋 List baselines", "list"),
            ("🧹 Clean benchmark data", "clean"),
            ("🔙 Back to main menu", "back"),
        ]

        while True:
            choice = self._get_choice(
                "Benchmark Actions:",
                benchmark_choices,
                "What would you like to do with benchmarks?",
            )

            if choice is None or choice == "back":
                break
            if choice == "run":
                baseline_name = self._get_text_input(
                    "Enter baseline name (optional):",
                    fallback_prompt="Enter baseline name (leave empty for auto-generated)",
                )
                self.cmd_benchmark("run", baseline_name=baseline_name or None)
            elif choice == "compare":
                self.cmd_benchmark("compare")
            elif choice == "list":
                self.cmd_benchmark("list")
            elif choice == "clean":
                self.cmd_benchmark("clean")


def main():
    """Main entry point."""
    # Check dev dependencies
    if not check_dev_dependencies():
        print("❌ Cannot run without required dependencies. Exiting.")
        sys.exit(1)

    dev = DevScript()

    # Check if we're in the right directory
    if (
        not (dev.project_root / "pyproject.toml").exists()
        and not (dev.project_root / "setup.py").exists()
    ):
        dev._print_warning("Not in a Python project directory?")

    # If no arguments, run interactive mode
    if len(sys.argv) == 1:
        dev.interactive_mode()
        return

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Development helper script for mplhep",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Test command
    test_parser = subparsers.add_parser(
        "test", help="Run pytest with matplotlib comparison"
    )
    test_parser.add_argument(
        "-n",
        "--jobs",
        type=int,
        default=dev.default_jobs,
        help=f"Number of parallel jobs (default: {dev.default_jobs})",
    )

    test_parser.add_argument(
        "-k", "--filter", type=str, help="Run only tests matching pattern"
    )
    test_parser.add_argument(
        "--skip-cleanup",
        action="store_true",
        help="Keep existing pytest_results directory",
    )

    # Benchmark command
    benchmark_parser = subparsers.add_parser(
        "benchmark", help="Run performance benchmarks"
    )
    benchmark_parser.add_argument(
        "action",
        choices=["run", "compare", "list", "clean"],
        help="Benchmark action to perform",
    )
    benchmark_parser.add_argument(
        "--save", type=str, help="Save benchmark results with custom name"
    )
    benchmark_parser.add_argument(
        "--with", dest="compare_with", type=str, help="Compare with specific baseline"
    )

    # Docs command
    docs_parser = subparsers.add_parser("docs", help="Build or serve documentation")
    docs_parser.add_argument(
        "action",
        choices=["build", "serve"],
        default="build",
        nargs="?",
        help="Documentation action (default: build)",
    )
    docs_parser.add_argument(
        "--port", type=int, default=8000, help="Port for serve command (default: 8000)"
    )
    docs_parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Skip --clean flag for build command",
    )
    docs_parser.add_argument(
        "--fast",
        action="store_true",
        help="Fast mode: disable figure rendering for ~50x faster builds",
    )

    # Other commands
    subparsers.add_parser(
        "baseline", help="Generate baseline images for matplotlib tests"
    )
    subparsers.add_parser("clean", help="Clean up test artifacts")
    subparsers.add_parser("precommit", help="Run pre-commit hooks on all files")
    subparsers.add_parser("help", help="Show help")

    # Parse known arguments and collect unknown ones
    args, unknown_args = parser.parse_known_args()

    # Execute commands
    try:
        if args.command == "test":
            # Extract argument mappings dynamically from the test parser
            arg_mappings = {}
            test_parser = None
            for action in parser._subparsers._actions:
                if (
                    hasattr(action, "choices")
                    and action.choices
                    and "test" in action.choices
                ):
                    test_parser = action.choices["test"]
                    break

            if test_parser:
                for action in test_parser._actions:
                    if hasattr(action, "option_strings") and action.option_strings:
                        # Map each option string to (dest, type)
                        for option_str in action.option_strings:
                            arg_mappings[option_str] = (action.dest, action.type or str)

            # Handle arguments that might appear in unknown args and override script args
            filtered_unknown_args = []
            overrides = {}

            i = 0
            while i < len(unknown_args):
                arg = unknown_args[i]
                if arg in arg_mappings and i + 1 < len(unknown_args):
                    # Found a known argument with a value, try to extract it
                    attr_name, parser_func = arg_mappings[arg]
                    try:
                        overrides[attr_name] = parser_func(unknown_args[i + 1])
                        i += 2  # Skip both the argument and its value
                    except (ValueError, TypeError):
                        # Not a valid value for this argument type, keep it in unknown args
                        filtered_unknown_args.append(unknown_args[i])
                        i += 1
                else:
                    filtered_unknown_args.append(unknown_args[i])
                    i += 1

            # Use overrides if provided, otherwise use parsed args
            final_jobs = overrides.get("jobs", args.jobs)
            final_filter = overrides.get("filter", args.filter)

            success = dev.cmd_test(
                jobs=final_jobs,
                filter_pattern=final_filter,
                skip_cleanup=args.skip_cleanup,
                extra_args=filtered_unknown_args,
            )
        elif args.command == "baseline":
            success = dev.cmd_baseline()
        elif args.command == "benchmark":
            baseline_name = getattr(args, "save", None)
            compare_with = getattr(args, "compare_with", None)
            success = dev.cmd_benchmark(args.action, baseline_name, compare_with)
        elif args.command == "docs":
            clean = not getattr(args, "no_clean", False)
            fast = getattr(args, "fast", False)
            success = dev.cmd_docs(args.action, args.port, clean, fast, unknown_args)
        elif args.command == "clean":
            success = dev.cmd_clean()
        elif args.command == "precommit":
            success = dev.cmd_precommit(extra_args=unknown_args)
        elif args.command == "help":
            dev.show_help()
            success = True
        else:
            parser.print_help()
            success = False

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        dev._print_warning("\nOperation cancelled")
        sys.exit(1)


if __name__ == "__main__":
    main()

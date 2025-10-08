"""
Development helper script for mplhep. Vibe-coded.

Usage: ./dev [command] [options] or ./dev for interactive mode
"""

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

try:
    import questionary
    from questionary import Style

    HAS_QUESTIONARY = True
except ImportError:
    questionary = None  # type: ignore[assignment]
    Style = None  # type: ignore[assignment]
    HAS_QUESTIONARY = False


def check_and_install_dev_dependencies() -> bool:
    """Check if questionary is available and install all dependencies if not."""
    if HAS_QUESTIONARY:
        return True

    print("\n🔧 Missing development dependencies (questionary)")
    print(
        '📦 Install command:\n    python -m pip install --upgrade --editable ".[all]"'
    )

    try:
        response = input("\nRun install Command? [Y/n]: ").strip().lower()
        if response in ["", "y", "yes"]:
            print("\n🔄 Installing all dependencies...")
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    "--editable",
                    ".[all]",
                ],
                check=True,
            )
            if result.returncode == 0:
                print("✅ All dependencies installed successfully!")
                return True
            print("❌ Failed to install dependencies")
            return False
        print("⚠️  Skipping dependency installation")
        return False
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False
    except KeyboardInterrupt:
        print("\n⚠️  Installation cancelled")
        return False


class DevScript:
    """Main development script class."""

    def __init__(self):
        self.default_jobs = self._get_default_jobs()
        self.project_root = Path.cwd()

    def _get_default_jobs(self) -> int:
        """Get default number of parallel jobs (half of CPU cores)."""
        try:
            cpu_count = os.cpu_count()
            if cpu_count is None:
                return 4  # fallback
            return max(1, cpu_count // 2)
        except (TypeError, AttributeError):
            return 4  # fallback

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

    def _run_command(self, cmd: List[str], cwd: Optional[Path] = None) -> bool:
        """Run a command and return True if successful."""
        try:
            self._print_header(f"Running: {' '.join(cmd)}")
            separator = 3 * ("=" * self._get_terminal_width() + "\n")
            print(separator)
            result = subprocess.run(cmd, cwd=cwd or self.project_root, check=True)
            print(separator)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            self._print_error(f"Command failed with exit code {e.returncode}")
            return False
        except FileNotFoundError:
            self._print_error(f"Command not found: {cmd[0]}")
            return False

    def _show_summary(self, items: List[Path], title: str) -> None:
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

    def _find_files_to_clean(self) -> List[Path]:
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
                for item in self.project_root.glob(target):
                    items_to_clean.append(item)
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
        jobs: Optional[int] = None,
        filter_pattern: Optional[str] = None,
        skip_cleanup: bool = False,
    ) -> bool:
        """Run pytest with matplotlib comparison."""
        if jobs is None:
            jobs = self.default_jobs

        # Handle pytest_results cleanup (only for direct command-line usage)
        if not skip_cleanup:
            pytest_results = self.project_root / "pytest_results"
            if pytest_results.exists():
                if self._confirm(
                    "Remove existing pytest_results/ directory?", default=True
                ):
                    self._print_warning(
                        "Removing existing pytest_results/ directory..."
                    )
                    shutil.rmtree(pytest_results)
                    self._print_success("Removed pytest_results/")
                else:
                    self._print_warning("Keeping existing pytest_results/")

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
            "-n",
            str(jobs),
        ]

        if filter_pattern:
            cmd.extend(["-k", filter_pattern])

        # Show the exact command and allow modification
        modified_cmd_str = questionary.text(
            "Confirm command (editable):",
            default=" ".join(cmd),
            style=self._get_style(),
        ).ask()
        if modified_cmd_str is None:
            return False

        if modified_cmd_str and modified_cmd_str.strip():
            try:
                cmd = shlex.split(modified_cmd_str)
            except ValueError as e:
                self._print_error(f"Invalid command syntax: {e}")
                return False

        success = self._run_command(cmd)

        if success:
            self._print_success("Tests completed successfully!")
        else:
            self._print_error("Tests failed!")

        return success

    def cmd_baseline(self) -> bool:
        """Generate baseline images for matplotlib comparison tests."""
        self._print_header("Generating Baseline Images")

        # Ask for baseline directory path
        if HAS_QUESTIONARY and questionary is not None:
            baseline_path = questionary.text(
                "Enter baseline directory path:",
                default="tests/baseline",
                style=self._get_style(),
            ).ask()
            if baseline_path is None:
                self._print_warning("Baseline generation cancelled")
                return False

            if not baseline_path.strip():
                baseline_path = "tests/baseline"
                self._print_warning(
                    "Empty path provided, using default: tests/baseline"
                )
        else:
            # Fallback for when questionary is not available
            baseline_path = input(
                "Enter baseline directory path [tests/baseline]: "
            ).strip()
            if not baseline_path:
                baseline_path = "tests/baseline"

        # Check if directory exists and warn about overwriting
        baseline_dir = Path(baseline_path)
        if baseline_dir.exists() and any(baseline_dir.iterdir()):
            self._print_warning(
                f"Directory '{baseline_path}' exists and contains files!"
            )
            self._print_warning("Existing baseline images will be overwritten.")
            if not self._confirm("Continue with baseline generation?", default=False):
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

        # Show the command and allow modification
        modified_cmd_str = questionary.text(
            "Confirm command (editable):",
            default=" ".join(cmd),
            style=self._get_style(),
        ).ask()
        if modified_cmd_str is None:
            return False

        if modified_cmd_str and modified_cmd_str.strip():
            try:
                cmd = shlex.split(modified_cmd_str)
            except ValueError as e:
                self._print_error(f"Invalid command syntax: {e}")
                return False

        success = self._run_command(cmd)

        if success:
            self._print_success("Baseline generation completed successfully!")
            self._print_warning(
                "Only include actually modified baseline images in your PR!"
            )
            self._print_warning("Review generated baselines before committing.")
        else:
            self._print_error("Baseline generation failed!")

        return success

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
            except OSError as e:
                self._print_error(f"Failed to remove {item}: {e}")

        if len(items_to_clean) > 10:
            self._print_success(
                f"Successfully removed {removed_count}/{len(items_to_clean)} items"
            )

        return True

    def cmd_precommit(self) -> bool:
        """Run pre-commit hooks on all files."""
        # Check if pre-commit is installed
        try:
            result = subprocess.run(
                ["pre-commit", "--version"], capture_output=True, text=True, check=True
            )
            self._print_success(f"Pre-commit version: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self._print_error("pre-commit not found!")
            install_precommit = self._confirm("Install pre-commit?", default=True)
            if install_precommit:
                install_cmd = [sys.executable, "-m", "pip", "install", "pre-commit"]
                if self._run_command(install_cmd):
                    self._print_success("Pre-commit installed successfully!")
                else:
                    self._print_error("Failed to install pre-commit")
                    return False
            else:
                self._print_warning("Pre-commit is required to run hooks")
                return False

        # Check if .pre-commit-config.yaml exists
        precommit_config = self.project_root / ".pre-commit-config.yaml"
        if not precommit_config.exists():
            self._print_warning("No .pre-commit-config.yaml found")
            create_config = self._confirm(
                "Install pre-commit hooks for this repository?", default=True
            )
            if create_config:
                install_cmd = ["pre-commit", "install"]
                if self._run_command(install_cmd):
                    self._print_success("Pre-commit hooks installed!")
                else:
                    self._print_error("Failed to install pre-commit hooks")
                    return False
            else:
                self._print_warning("Cannot run pre-commit without configuration")
                return False

        # Run pre-commit on all files
        cmd = ["pre-commit", "run", "--all-files"]

        # Show the command and allow modification
        modified_cmd_str = questionary.text(
            "Confirm command (editable):",
            default=" ".join(cmd),
            style=self._get_style(),
        ).ask()
        if modified_cmd_str is None:
            return False

        if modified_cmd_str and modified_cmd_str.strip():
            try:
                cmd = shlex.split(modified_cmd_str)
            except ValueError as e:
                self._print_error(f"Invalid command syntax: {e}")
                return False

        success = self._run_command(cmd)

        if success:
            self._print_success("Pre-commit hooks completed successfully!")
        else:
            self._print_warning("Pre-commit hooks found issues (this is normal)")
            self._print_warning("Review the output above and fix any issues")

        return True

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
  clean     Clean up test artifacts
  precommit Run pre-commit hooks on all files
  help      Show this help

Test command options:
  -j, --jobs N     Number of parallel jobs (default: {self.default_jobs})
  -k, --filter     Run only tests matching pattern
  --skip-cleanup   Keep existing pytest_results directory

Examples:
  ./dev test -j 4                 # Run tests with 4 jobs
  ./dev test -k "test_basic"      # Run only tests matching "test_basic"
  ./dev clean                     # Clean up test artifacts
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

    def _get_test_modules(self) -> List[str]:
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
        if not HAS_QUESTIONARY or questionary is None:
            # Fallback mode - basic implementation
            print("\n🔧 Configure Test Run")
            print("Interactive mode requires questionary. Using basic mode.")
            jobs = self.default_jobs
            filter_pattern = None
            return {"jobs": jobs, "filter_pattern": filter_pattern}

        print("\n🔧 Configure Test Run")

        # Jobs selection with choices
        jobs_choice = questionary.select(
            "Parallel execution mode:",
            choices=[
                questionary.Choice(
                    f"🚀 Default ({self.default_jobs} cores)", "default"
                ),
                questionary.Choice("🔄 No parallelism (1 core)", "none"),
                questionary.Choice("⚙️  Custom number", "custom"),
            ],
            style=self._get_style(),
        ).ask()

        if jobs_choice == "default":
            jobs = self.default_jobs
        elif jobs_choice == "none":
            jobs = 1
        elif jobs_choice == "custom":
            jobs_input = questionary.text(
                "Enter number of parallel jobs:",
                default=str(self.default_jobs),
                style=self._get_style(),
            ).ask()
            if jobs_input is None:
                jobs = self.default_jobs
                self._print_warning(f"Input cancelled, using default: {jobs}")
            else:
                try:
                    jobs = int(jobs_input)
                    if jobs < 1:
                        self._print_warning("Jobs must be at least 1, using 1")
                        jobs = 1
                except (ValueError, TypeError):
                    jobs = self.default_jobs
                    self._print_warning(f"Invalid jobs value, using default: {jobs}")
        else:
            jobs = self.default_jobs

        # Test selection with choices
        test_choice = questionary.select(
            "Test selection mode:",
            choices=[
                questionary.Choice("🎯 Run all tests", "all"),
                questionary.Choice("📦 Select submodules", "submodules"),
                questionary.Choice("🔍 Custom pattern", "custom"),
            ],
            style=self._get_style(),
        ).ask()

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
            print("  • test_basic                    - Run tests matching 'test_basic'")
            print("  • test_plot                     - Run tests matching 'test_plot'")
            print(
                "  • test_basic or test_plot       - Run tests matching either pattern"
            )
            print(
                "  • test_basic and not slow       - Run test_basic but exclude 'slow' tests"
            )
            print("  • TestClass                     - Run all tests in TestClass")
            print("  • TestClass::test_method        - Run specific test method")
            print(
                "  • test_*.py                     - Run tests in files matching pattern"
            )

            filter_pattern = questionary.text(
                "Enter custom test pattern:", style=self._get_style()
            ).ask()
            if filter_pattern is None:
                self._print_warning("Input cancelled - all tests will be run")
                filter_pattern = None
            elif not filter_pattern or not filter_pattern.strip():
                self._print_warning("No pattern entered - all tests will be run")
                filter_pattern = None

        return {
            "jobs": jobs,
            "filter_pattern": filter_pattern,
        }

    def interactive_mode(self) -> None:
        """Run in interactive mode with questionary menu."""
        if not HAS_QUESTIONARY or questionary is None:
            print("\n❌ Interactive mode requires questionary.")
            print('Install with: python -m pip install --upgrade --editable ".[all]"')
            return

        print("\n" + "=" * 60)
        print("🚀 mplhep Development Helper - Interactive Mode")
        print("=" * 60)

        while True:
            try:
                choice = questionary.select(
                    "What would you like to do?",
                    choices=[
                        questionary.Choice("🔍 Run Pre-commit", "precommit"),
                        questionary.Choice("🧪 Run Tests", "test"),
                        questionary.Choice("🖼️ Generate Baselines", "baseline"),
                        questionary.Choice("🧹 Clean Artifacts", "clean"),
                        questionary.Choice("📖 Show Help", "help"),
                        questionary.Choice("🚪 Exit", "exit"),
                    ],
                    style=self._get_style(),
                ).ask()

                if choice is None or choice == "exit":
                    print("\n👋 Goodbye!")
                    break
                if choice == "test":
                    # Handle pytest_results cleanup first
                    pytest_results = self.project_root / "pytest_results"
                    if pytest_results.exists():
                        if self._confirm(
                            "Remove existing pytest_results/ directory?", default=True
                        ):
                            self._print_warning(
                                "Removing existing pytest_results/ directory..."
                            )
                            shutil.rmtree(pytest_results)
                            self._print_success("Removed pytest_results/")
                        else:
                            self._print_warning("Keeping existing pytest_results/")

                    options = self._interactive_test_options()
                    self.cmd_test(**options, skip_cleanup=True)
                elif choice == "baseline":
                    self.cmd_baseline()
                elif choice == "clean":
                    self.cmd_clean()
                elif choice == "precommit":
                    self.cmd_precommit()
                elif choice == "help":
                    self.show_help()

                # Continue to main menu (no additional prompt needed)

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break


def main():
    """Main entry point."""
    # Check and install dev dependencies if needed
    if not check_and_install_dev_dependencies():
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
        "-j",
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

    # Other commands
    subparsers.add_parser(
        "baseline", help="Generate baseline images for matplotlib tests"
    )
    subparsers.add_parser("clean", help="Clean up test artifacts")
    subparsers.add_parser("help", help="Show help")

    # Parse arguments
    args = parser.parse_args()

    # Execute commands
    try:
        if args.command == "test":
            success = dev.cmd_test(
                jobs=args.jobs,
                filter_pattern=args.filter,
                skip_cleanup=args.skip_cleanup,
            )
        elif args.command == "baseline":
            success = dev.cmd_baseline()
        elif args.command == "clean":
            success = dev.cmd_clean()
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

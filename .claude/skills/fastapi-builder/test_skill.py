#!/usr/bin/env python3
"""
Test script for FastAPI Builder skill
"""

import os
import tempfile
import subprocess
import sys
from pathlib import Path


def test_skill_structure():
    """Test that the skill has the correct structure."""
    skill_path = Path("skills/fastapi-builder")

    # Check main skill file exists
    assert (skill_path / "SKILL.md").exists(), "SKILL.md file is missing"

    # Check required directories exist
    assert (skill_path / "references").exists(), "references directory is missing"
    assert (skill_path / "scripts").exists(), "scripts directory is missing"
    assert (skill_path / "assets").exists(), "assets directory is missing"

    # Check reference files exist
    reference_files = ["models.md", "crud.md", "auth.md", "database.md"]
    for ref_file in reference_files:
        assert (skill_path / "references" / ref_file).exists(), f"{ref_file} is missing"

    # Check asset files exist
    asset_files = ["model-template.py", "auth-template.py", "requirements.txt"]
    for asset_file in asset_files:
        assert (skill_path / "assets" / asset_file).exists(), f"{asset_file} is missing"

    # Check script files exist
    script_files = ["init-fastapi-project.py"]
    for script_file in script_files:
        assert (skill_path / "scripts" / script_file).exists(), f"{script_file} is missing"

    print("✅ Skill structure is valid")


def test_script_executability():
    """Test that the init script is executable."""
    script_path = Path("skills/fastapi-builder/scripts/init-fastapi-project.py")

    # Check if the script has a shebang
    with open(script_path, 'r') as f:
        first_line = f.readline().strip()
        assert first_line.startswith("#!/usr/bin/env python"), f"Script doesn't have proper shebang: {first_line}"

    # Make sure it's executable (on Unix-like systems)
    if os.name != 'nt':  # Skip on Windows
        st = os.stat(script_path)
        assert st.st_mode & 0o111, "Script is not executable"

    print("✅ Script executability is valid")


def test_project_creation():
    """Test that the project creation script works."""
    script_path = Path("skills/fastapi-builder/scripts/init-fastapi-project.py")

    with tempfile.TemporaryDirectory() as tmp_dir:
        temp_path = Path(tmp_dir)

        # Run the script to create a test project
        result = subprocess.run([
            sys.executable, str(script_path), "test-project", "--path", str(temp_path)
        ], capture_output=True, text=True)

        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Check that project was created
        project_path = temp_path / "test-project"
        assert project_path.exists(), "Test project was not created"

        # Check essential files exist
        essential_files = [
            "app/main.py",
            "requirements.txt",
            ".env",
            ".gitignore",
            "README.md"
        ]

        for file_path in essential_files:
            assert (project_path / file_path).exists(), f"Essential file {file_path} is missing"

        print("✅ Project creation test passed")


def main():
    """Run all tests."""
    print("Testing FastAPI Builder skill...")

    test_skill_structure()
    test_script_executability()
    test_project_creation()

    print("\n🎉 All tests passed! The FastAPI Builder skill is ready to use.")


if __name__ == "__main__":
    main()
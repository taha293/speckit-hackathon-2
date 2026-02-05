#!/usr/bin/env python3
"""
Validation script for SQLModel Builder skill
"""

import os
from pathlib import Path

def validate_skill():
    """Validate that all required skill files were created."""
    skill_path = Path("E:/Python/hackathon2/.claude/skills/sqlmodel-builder")

    # Check if skill directory exists
    if not skill_path.exists():
        print("ERROR: Skill directory does not exist")
        return False

    print("SUCCESS: Skill directory exists")

    # Check required files
    required_files = [
        "SKILL.md",
        "references/patterns.md",
        "scripts/setup_project.py",
        "scripts/test_setup.py",
        "assets/templates.md"
    ]

    all_good = True

    for file_path in required_files:
        full_path = skill_path / file_path
        if not full_path.exists():
            print(f"ERROR: Missing required file: {file_path}")
            all_good = False
        else:
            print(f"SUCCESS: Found required file: {file_path}")

    # Validate SKILL.md has proper frontmatter
    skill_md = skill_path / "SKILL.md"
    with open(skill_md, 'r') as f:
        content = f.read()

    if "---" in content and "name: sqlmodel-builder" in content:
        print("SUCCESS: SKILL.md has proper frontmatter")
    else:
        print("ERROR: SKILL.md missing proper frontmatter")
        all_good = False

    # Check for important sections in SKILL.md
    important_sections = [
        "When to Use This Skill",
        "Model Creation",
        "Database Setup",
        "Security Best Practices"
    ]

    for section in important_sections:
        if section in content:
            print(f"SUCCESS: Found important section: {section}")
        else:
            print(f"ERROR: Missing important section: {section}")
            all_good = False

    return all_good

if __name__ == "__main__":
    print("Validating SQLModel Builder skill...")
    if validate_skill():
        print("\nAll validations passed! SQLModel Builder skill is ready.")
    else:
        print("\nSome validations failed. Please check the issues above.")
# Guidelines and Instructions

## Background
- The project is a fork of the open-source project `sqlacodegen` at https://github.com/agronholm/sqlacodegen.
- This fork is hosted on GitHub at https://github.com/Samplead/sqlacodegen.
- The working branch is `feature/declarative-str-enum-support`.
- The purpose of this fork is to develop the feature that described in the `feature-docs/PRD.md` file.

## Differences between the original project and this fork
    - `tests/test_str_enum_flag.py` (added): This file contains the tests for the feature.
    - `src/sqlacodegen/generators.py` (modified): THIS IS THE MAIN FILE OF THE PACKAGE. All the changes that I did to this file are listed in the `feature-docs/CHANGES_SUMMARY.md` file.
    - `feature-docs/` (temporary): This directory contains the documentation for the feature. All the files in this directory will be deleted before opening a PR to the original project.

## Framework-specific Guidelines
- Use `uv` (or `uvx`, when appropriate) for running commands.
- For linting and type checking, use `ruff` and `basedpyright`.
- For formatting and import sorting, use `ruff`.

## Guidelines For Fixing Issues
- Before starting to work on the issue, you must read ALL the files in the `feature-docs` directory:
    - `CHANGES_SUMMARY.md`: Will give you the summary of the changes that have already been made to the codebase.
    - `PRD.md`: Will give you the context and the requirements for the feature.
    - `ISSUE.md`: Will give you the description of the issue.
    - `HOW-TO-TEST.md`: Will give you the instructions for testing the feature.
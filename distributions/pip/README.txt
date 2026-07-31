PIP - Python package install
==============================

For users who have Python installed.

Editable install:
  cd release
  python -m pip install -e .
  net-defense-console

Or install a built wheel from this folder:
  python -m pip install net_defense_ops_console-*.whl

Build wheel into this folder:
  powershell -ExecutionPolicy Bypass -File release\packaging\build_pip.ps1

Package metadata: ..\release\pyproject.toml

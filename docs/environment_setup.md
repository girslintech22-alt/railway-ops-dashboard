# Environment Setup (Windows PowerShell)

## 1) Create virtual environment

```powershell
python -m venv .venv
```

## 2) Activate virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

## 3) Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4) Verify interpreter and environment

```powershell
python -c "import sys; print(sys.executable)"
python -m pip --version
python -m pip list
python storage/environment_check.py
```

## 5) Run tests

```powershell
python -m pytest
```

## 6) Run local snapshot-based pipeline (no API calls)

```powershell
python -c "from processing.train_processor import process_all_train_snapshots; from processing.route_processor import process_all_route_snapshots; from analytics.kpi_engine import generate_kpi_report; process_all_train_snapshots(); process_all_route_snapshots(); print(generate_kpi_report())"
```

## VS Code interpreter validation

1. Open Command Palette (`Ctrl+Shift+P`).
2. Run `Python: Select Interpreter`.
3. Choose the interpreter under `.venv` for this workspace.
4. Confirm terminal interpreter:

```powershell
python -c "import sys; print(sys.executable)"
```

5. Confirm required packages are installed in active interpreter:

```powershell
python -m pip show requests python-dotenv pytest
```

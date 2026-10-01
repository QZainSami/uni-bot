# Uni-Bot (Bahria CMS Survey Automator)

An automation script that logs into the Bahria University Student CMS portal and automatically completes pending Quality Assurance (QA) surveys using Selenium and Chrome[cite: 1].

## Features

- **Automated Login:** Logs in using your student enrollment credentials and campus selection[cite: 1].
- **Survey Discovery:** Scans the Quality Assurance dashboard for all pending survey links[cite: 1].
- **Smart Form Autofill:** Executes client-side JavaScript to select answers for 5-point scale rating questions and demographic options (e.g., employment status, gender/age fallbacks)[cite: 1].
- **Dynamic Submission:** Automatically identifies the submit/save buttons and proceeds to the next survey[cite: 1].

## Prerequisites

- [Google Chrome](https://www.google.com/chrome/) installed.
- [uv](https://docs.astral.sh/uv/) (recommended) or Python 3.10+ with `pip`[cite: 1].

## Configuration

Open `bot.py` in an editor and update your student details[cite: 1]:

```python
# ==========================================
# CONFIGURATION - ENTER YOUR DETAILS HERE
# ==========================================
USERNAME = "02-134242-111"        # Your enrollment ID
PASSWORD = "YOUR_PASSWORD_HERE"    # Your CMS password
INSTITUTE_VALUE = "2"              # "2" is Karachi Campus
```

## How to Run

### Method 1: Using `uv` (Recommended)

Run the script from your terminal inside the project directory[cite: 1]:

```bash
uv run bot.py
```

`uv` automatically handles virtual environment creation and package installation from `uv.lock`[cite: 1].

---

### Method 2: Standard Python (`pip`)

1. **Create and activate a virtual environment:**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS:**
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```

2. **Install dependencies:**
   ```bash
   pip install selenium
   ```

3. **Run the bot:**
   ```bash
   python bot.py
   ```

## Cleanup

To completely remove the local virtual environment and caches created by `uv`:

- **Delete local virtual environment:**
  - PowerShell: `Remove-Item -Recurse -Force .venv`
  - Linux/macOS: `rm -rf .venv`
- **Clean package download cache:**
  ```bash
  uv cache clean
  ```
- **Uninstall a uv-managed Python version (if installed via uv):**
  ```bash
  uv python uninstall 3.11
  ```

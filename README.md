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

## Alternative: Browser Console Script (No Python)

If you prefer not to run Python or Selenium, you can autofill surveys directly inside your browser:

1. Log in to your Bahria CMS portal manually.
2. Navigate to the pending surveys page or an individual survey.
3. Open your browser console (`F12` -> **Console** tab).
4. Paste the following snippet and press **Enter**:

```javascript
(async () => {
  const CONFIG = {
    neutral: /neutral/i,
    male: /^\s*male\s*$/i,
    comment: "",        // Optional comment text
    submit: true,       // Set false to review before submission
    delay: 1500
  };
  const sleep = ms => new Promise(r => setTimeout(r, ms));

  function labelText(el) {
    const doc = el.ownerDocument;
    let t = "";
    if (el.id) { const l = doc.querySelector(`label[for="${el.id}"]`); if (l) t = l.textContent; }
    if (!t.trim()) { const l = el.closest("label"); if (l) t = l.textContent; }
    if (!t.trim() && el.nextSibling) t = el.nextSibling.textContent || "";
    if (!t.trim()) {
      const td = el.closest("td");
      const table = td && td.closest("table");
      const head = table && table.querySelector("thead tr, tr");
      if (head && head.children[td.cellIndex]) t = head.children[td.cellIndex].textContent;
    }
    if (!t.trim()) t = el.title || el.getAttribute("aria-label") || "";
    return t.trim();
  }

  function fillDoc(doc) {
    let count = 0;
    const groups = {};
    doc.querySelectorAll('input[type="radio"]').forEach(r => (groups[r.name] ||= []).push(r));
    Object.values(groups).forEach(g => {
      const texts = g.map(labelText);
      let i = texts.findIndex(t => CONFIG.male.test(t));
      if (i < 0) i = texts.findIndex(t => CONFIG.neutral.test(t));
      if (i < 0 && g.length >= 3) i = Math.floor(g.length / 2);
      if (i >= 0) { g[i].checked = true; g[i].click(); count++; }
    });

    doc.querySelectorAll("select").forEach(s => {
      const opts = [...s.options];
      let o = opts.find(x => CONFIG.male.test(x.text));
      if (!o) o = opts.find(x => CONFIG.neutral.test(x.text));
      if (o) {
        s.value = o.value;
        s.dispatchEvent(new Event("change", { bubbles: true }));
        count++;
      }
    });

    if (CONFIG.comment) {
      doc.querySelectorAll("textarea").forEach(t => { if (!t.value.trim()) { t.value = CONFIG.comment; count++; } });
    }
    return count;
  }

  function findSubmit(doc) {
    return [...doc.querySelectorAll('input[type="submit"], input[type="button"], button, a.btn')]
      .find(b => /submit|save|finish|complete/i.test(b.value || b.textContent));
  }

  const links = [...document.querySelectorAll('a[href*="SurveyStudentCourseWise"]')].map(a => a.href);

  if (links.length) {
    console.log(`Found ${links.length} surveys`);
    for (const [idx, url] of links.entries()) {
      const f = document.createElement("iframe");
      f.style.cssText = "position:fixed;left:-9999px;width:1100px;height:700px";
      document.body.appendChild(f);
      await new Promise(r => { f.onload = r; f.src = url; });
      f.contentWindow.confirm = () => true;
      f.contentWindow.alert = () => {};
      await sleep(CONFIG.delay);
      const n = fillDoc(f.contentDocument);
      console.log(`#${idx + 1}: filled ${n} fields`);
      if (CONFIG.submit) {
        const btn = findSubmit(f.contentDocument);
        if (btn) {
          await new Promise(r => { f.onload = r; btn.click(); setTimeout(r, 8000); });
          console.log(`#${idx + 1}: submitted`);
        } else console.warn(`#${idx + 1}: submit button not found`);
      }
      f.remove();
    }
    console.log("Done. Refresh the page to check.");
    return;
  }

  console.log(`Filled ${fillDoc(document)} fields`);
  if (CONFIG.submit) { const b = findSubmit(document); if (b) b.click(); }
})();
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

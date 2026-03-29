---
name: xlsx
description: "Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modify existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas"
license: Proprietary. LICENSE.txt has complete terms
---

# Core Requirements

## Zero Formula Errors (ALL Excel Files)
Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)

## Preserve Existing Templates
When modifying existing files:
- Study and EXACTLY match existing format, style, and conventions
- Never impose standardized formatting on files with established patterns
- Existing template conventions ALWAYS override these guidelines

## Financial Models
For detailed financial modeling standards (color coding, number formatting, formula rules), see [financial-modeling-standards.md](financial-modeling-standards.md)

# XLSX Workflows

## Tool Selection
- **pandas**: Data analysis, visualization, bulk operations, simple data export
- **openpyxl**: Formulas, formatting, Excel-specific features, preserving existing files

LibreOffice is assumed installed for formula recalculation via `recalc.py`

## CRITICAL: Use Formulas, Not Hardcoded Values
Always use Excel formulas instead of calculating values in Python. This ensures spreadsheets remain dynamic.

❌ WRONG: `sheet['B10'] = df['Sales'].sum()` (hardcodes value)
✅ CORRECT: `sheet['B10'] = '=SUM(B2:B9)'` (dynamic formula)

## Standard Workflow
1. **Choose tool**: pandas for data, openpyxl for formulas/formatting
2. **Create/Load**: Create new workbook or load existing file
3. **Modify**: Add/edit data, formulas, and formatting
4. **Save**: Write to file
5. **Recalculate formulas** (MANDATORY if using formulas):
   ```bash
   python recalc.py output.xlsx
   ```
6. **Verify and fix errors**: Check JSON output for errors, fix them, recalculate again

## Quick Examples

### Reading/Analyzing Data
```python
import pandas as pd
df = pd.read_excel('file.xlsx')  # Read first sheet
df.head()  # Preview
df.describe()  # Statistics
```

### Creating New Files
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
sheet = wb.active
sheet['A1'] = 'Header'
sheet['B2'] = '=SUM(A1:A10)'  # Formula, not hardcoded value
sheet['A1'].font = Font(bold=True)
sheet.column_dimensions['A'].width = 20
wb.save('output.xlsx')
```

### Editing Existing Files
```python
from openpyxl import load_workbook
wb = load_workbook('existing.xlsx')
sheet = wb.active  # or wb['SheetName']
sheet['A1'] = 'New Value'
wb.save('modified.xlsx')
```

### Recalculating Formulas
```bash
python recalc.py output.xlsx 30
```

Returns JSON with error details:
```json
{
  "status": "success",  // or "errors_found"
  "total_errors": 0,
  "error_summary": {
    "#REF!": {"count": 2, "locations": ["Sheet1!B5"]}
  }
}
```

## Formula Verification Checklist
- [ ] Test 2-3 sample cell references before building full model
- [ ] Verify column mapping (column 64 = BL, not BK)
- [ ] Remember row offset (DataFrame row 5 = Excel row 6)
- [ ] Check for NaN values with `pd.notna()`
- [ ] Verify division denominators aren't zero (#DIV/0!)
- [ ] Test formulas on small sample before applying broadly

## Key Best Practices
- **openpyxl**: 1-based indexing (row=1, col=1 is A1)
- **data_only=True**: Reads values but DESTROYS formulas if saved - use carefully
- **Formulas**: Preserved but not evaluated - always use recalc.py after saving
- **Code style**: Write minimal, concise Python without verbose comments

For detailed examples and workflows, see [examples.md](examples.md)

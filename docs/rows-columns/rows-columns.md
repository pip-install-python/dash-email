---
name: Rows & Columns
description: Multi-column layouts that render as tables — the only layout email clients reliably support.
endpoint: /components/rows-columns
package: dash_email
icon: tabler:columns
category: Components
order: 3
lastmod: 2026-07-16
---

.. llms_copy::Rows & Columns

.. toc::

### Table-based layout

Flexbox and CSS grid don't survive most email clients. `EmailRow` and
`EmailColumn` render as an HTML `<table>` / `<td>` pair so multi-column
layouts hold together everywhere — set column widths with percentage styles.

.. exec::docs.rows-columns.rows_columns
    :code: false

Source code:

.. source::docs/rows-columns/rows_columns.py

---

### EmailRow

.. kwargs::EmailRow

---

### EmailColumn

.. kwargs::EmailColumn

---
name: Getting Started
description: Install dash-email and build your first email template in minutes.
endpoint: /getting-started
package: dash_email
icon: tabler:rocket
lastmod: 2026-07-16
---

.. llms_copy::Getting Started

.. toc::

### Installation

Install from PyPI:

```bash
pip install dash-email
```

dash-email requires **Python 3.9+** and **Dash 4.2+**.

---

### Your first email

Every email starts with the same skeleton: `Email` → `EmailBody` → `EmailContainer` → content.
The components render table-based, inline-styled HTML that survives Gmail, Outlook, and Apple Mail.

.. exec::docs.getting-started.quickstart
    :code: false

Source code:

.. source::docs/getting-started/quickstart.py

---

### Components are callback-ready

Every dash-email component is a first-class Dash component — give it an `id`
and update it from callbacks like any other component. Type in the input below
and watch the email headline update:

.. exec::docs.getting-started.interactive
    :code: false

Source code:

.. source::docs/getting-started/interactive.py

---

### The component set

| Category | Components |
|----------|------------|
| Structure | `Email`, `EmailHead`, `EmailPreview`, `EmailBody` |
| Layout    | `EmailContainer`, `EmailSection`, `EmailRow`, `EmailColumn` |
| Content   | `EmailHeading`, `EmailText`, `EmailButton`, `EmailLink` |
| Media     | `EmailImage`, `EmailDivider`, `EmailFont` |

---

### Styling rules for email

.. admonition::Email clients are not browsers
    :icon: tabler:alert-triangle
    :color: yellow

    Email clients strip `<style>` tags and ignore most modern CSS. dash-email
    components accept a `style` prop with camelCase CSS that is rendered inline —
    stick to inline styles, table-based layout (`EmailRow`/`EmailColumn`), and
    keep content width at 600px or less.

---

### Next steps

- Explore each component group in the sidebar — every page has isolated, runnable examples.
- Open the **Email Builder** to generate templates with AI, preview them live, and send test emails via Resend.

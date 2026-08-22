---
name: Email Structure
description: The root components every email template needs — Email, EmailHead, EmailPreview, and EmailBody.
endpoint: /components/email-structure
package: dash_email
icon: tabler:layout
lastmod: 2026-07-16
---

.. llms_copy::Email Structure

.. toc::

### Anatomy of an email

Four components form the skeleton of every template:

- `Email` — the root wrapper (equivalent to React Email's `Html`)
- `EmailHead` — metadata such as the document title and font imports
- `EmailPreview` — the snippet shown next to the subject line in the inbox, hidden in the body
- `EmailBody` — the visible content wrapper

.. exec::docs.email-structure.structure
    :code: false

Source code:

.. source::docs/email-structure/structure.py

---

### Email

.. kwargs::Email

---

### EmailHead

.. kwargs::EmailHead

---

### EmailPreview

.. kwargs::EmailPreview

---

### EmailBody

.. kwargs::EmailBody

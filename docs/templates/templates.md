---
name: Full Templates
description: Complete, copy-paste-ready email templates combining all the components.
endpoint: /templates
package: dash_email
icon: tabler:template
lastmod: 2026-07-16
---

.. llms_copy::Full Templates

.. toc::

### Newsletter

A classic three-section newsletter: branded header, article content with CTA,
and a compliance footer.

.. exec::docs.templates.newsletter
    :code: false

Source code:

.. source::docs/templates/newsletter.py

---

### Order confirmation

A transactional receipt using `EmailRow`/`EmailColumn` for line items and
totals.

.. exec::docs.templates.order_confirmation
    :code: false

Source code:

.. source::docs/templates/order_confirmation.py

---

### Build your own with AI

The **Email Builder** at `/email-builder` generates templates like these from a
plain-English prompt using Google Gemini, previews them live, and exports
ready-to-paste `dash_email` code.

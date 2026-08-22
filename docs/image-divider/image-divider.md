---
name: Image & Divider
description: Images with explicit dimensions and horizontal rules for separating content.
endpoint: /components/image-divider
package: dash_email
icon: tabler:photo
lastmod: 2026-07-16
---

.. llms_copy::Image & Divider

.. toc::

### Media & separation

`EmailImage` renders an `<img>` with explicit dimensions — required for stable
layouts since many clients block remote images by default. `EmailDivider`
renders an `<hr>` for visual separation between blocks.

.. exec::docs.image-divider.image_divider
    :code: false

Source code:

.. source::docs/image-divider/image_divider.py

---

### EmailImage

.. kwargs::EmailImage

---

### EmailDivider

.. kwargs::EmailDivider

---
name: Custom Fonts
description: Load web fonts with graceful fallbacks using EmailFont.
endpoint: /components/fonts
package: dash_email
icon: tabler:letter-case
lastmod: 2026-07-16
---

.. llms_copy::Custom Fonts

.. toc::

### Web fonts in email

`EmailFont` lives inside `EmailHead` and declares a web font plus a fallback
family. Support varies — Apple Mail and iOS load web fonts, Gmail and Outlook
fall back — so always pick a similar-looking system fallback.

.. exec::docs.fonts.fonts
    :code: false

Source code:

.. source::docs/fonts/fonts.py

---

### EmailFont

.. kwargs::EmailFont

---
name: Heading & Text
description: Typography components for email — headings h1-h6 and paragraph text.
endpoint: /components/heading-text
package: dash_email
icon: tabler:typography
lastmod: 2026-07-16
---

.. llms_copy::Heading & Text

.. toc::

### Typography

`EmailHeading` renders `h1`–`h6` elements via the `as_` prop; `EmailText`
renders paragraphs. Both take inline styles through the `style` prop.

.. admonition::Why as_ and not as?
    :icon: tabler:info-circle
    :color: blue

    `as` is a reserved word in Python, so the prop is exposed as `as_` —
    the same convention Dash uses for `class` → `className`.

.. exec::docs.heading-text.heading_text
    :code: false

Source code:

.. source::docs/heading-text/heading_text.py

---

### EmailHeading

.. kwargs::EmailHeading

---

### EmailText

.. kwargs::EmailText

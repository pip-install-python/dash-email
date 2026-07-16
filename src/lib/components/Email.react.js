import React from 'react';
import PropTypes from 'prop-types';

/**
 * Email is the root wrapper component for email templates.
 * Renders as an HTML document structure suitable for email preview.
 */
const Email = ({
    id,
    children,
    lang = 'en',
    dir = 'ltr',
    style = {},
    setProps
}) => {
    return (
        <div
            id={id}
            lang={lang}
            dir={dir}
            style={{
                fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
                ...style
            }}
            data-email-component="html"
        >
            {children}
        </div>
    );
};

Email.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The children of this component (EmailHead, EmailPreview, EmailBody, etc.)
     */
    children: PropTypes.node,

    /**
     * Language of the email content.
     */
    lang: PropTypes.string,

    /**
     * Text direction of the email content.
     */
    dir: PropTypes.oneOf(['ltr', 'rtl']),

    /**
     * Inline styles for the html element.
     */
    style: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default Email;
import React from 'react';
import PropTypes from 'prop-types';

/**
 * EmailLink renders a hyperlink in the email.
 */
const EmailLink = ({
    id,
    children,
    href,
    target = '_blank',
    style = {},
    setProps
}) => {
    return (
        <a
            id={id}
            href={href}
            target={target}
            style={style}
            data-email-component="link"
        >
            {children}
        </a>
    );
};

EmailLink.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The link text/content.
     */
    children: PropTypes.node,

    /**
     * The URL to navigate to when clicked.
     */
    href: PropTypes.string.isRequired,

    /**
     * Where to open the link (_blank, _self, etc.)
     */
    target: PropTypes.string,

    /**
     * Inline styles for the link.
     */
    style: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default EmailLink;
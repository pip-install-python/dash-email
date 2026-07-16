import React from 'react';
import PropTypes from 'prop-types';

/**
 * EmailButton renders a styled link that looks like a button.
 */
const EmailButton = ({
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
            style={{
                display: 'inline-block',
                textDecoration: 'none',
                textAlign: 'center',
                ...style
            }}
            data-email-component="button"
        >
            {children}
        </a>
    );
};

EmailButton.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The button label/content.
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
     * Inline styles for the button.
     */
    style: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default EmailButton;

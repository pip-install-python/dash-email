import React from 'react';
import PropTypes from 'prop-types';

/**
 * EmailText renders paragraph text with proper spacing.
 */
const EmailText = ({
    id,
    children,
    style = {},
    setProps
}) => {
    return (
        <p
            id={id}
            style={{
                margin: '16px 0',
                ...style
            }}
            data-email-component="text"
        >
            {children}
        </p>
    );
};

EmailText.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The text content.
     */
    children: PropTypes.node,

    /**
     * Inline styles for the text.
     */
    style: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default EmailText;
import React from 'react';
import PropTypes from 'prop-types';

/**
 * EmailBody wraps the main content of the email.
 */
const EmailBody = ({
    id,
    children,
    style = {},
    setProps
}) => {
    return (
        <div
            id={id}
            style={{
                margin: 0,
                padding: 0,
                width: '100%',
                ...style
            }}
            data-email-component="body"
        >
            {children}
        </div>
    );
};

EmailBody.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The children of this component (EmailContainer, EmailSection, etc.)
     */
    children: PropTypes.node,

    /**
     * Inline styles for the body element.
     */
    style: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default EmailBody;
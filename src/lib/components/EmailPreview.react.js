import React from 'react';
import PropTypes from 'prop-types';

/**
 * EmailPreview renders preview text that appears in the inbox
 * before the email is opened. Hidden in the actual email body.
 */
const EmailPreview = ({
    id,
    children,
    setProps
}) => {
    // Preview text is hidden but read by email clients
    return (
        <div
            id={id}
            style={{
                display: 'none',
                fontSize: '1px',
                lineHeight: '1px',
                maxHeight: 0,
                maxWidth: 0,
                opacity: 0,
                overflow: 'hidden'
            }}
            data-email-component="preview"
        >
            {children}
        </div>
    );
};

EmailPreview.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The preview text to display in email client inboxes.
     */
    children: PropTypes.node,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default EmailPreview;
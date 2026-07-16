import React from 'react';
import PropTypes from 'prop-types';

/**
 * EmailHead contains metadata for the email such as fonts.
 * In preview mode, this renders as a hidden container.
 */
const EmailHead = ({
    id,
    children,
    setProps
}) => {
    return (
        <div
            id={id}
            style={{ display: 'none' }}
            data-email-component="head"
        >
            {children}
        </div>
    );
};

EmailHead.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The children of this component (EmailFont, style elements, etc.)
     */
    children: PropTypes.node,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default EmailHead;
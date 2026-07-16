import React from 'react';
import PropTypes from 'prop-types';

/**
 * EmailDivider renders a horizontal line/divider.
 */
const EmailDivider = ({
    id,
    style = {},
    setProps
}) => {
    return (
        <hr
            id={id}
            style={{
                border: 'none',
                borderTop: '1px solid #eaeaea',
                margin: '16px 0',
                ...style
            }}
            data-email-component="divider"
        />
    );
};

EmailDivider.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * Inline styles for the divider.
     */
    style: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default EmailDivider;
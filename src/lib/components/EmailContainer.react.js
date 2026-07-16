import React from 'react';
import PropTypes from 'prop-types';

/**
 * EmailContainer centers content horizontally with a max-width.
 */
const EmailContainer = ({
    id,
    children,
    style = {},
    setProps
}) => {
    return (
        <div
            id={id}
            style={{
                maxWidth: '600px',
                margin: '0 auto',
                ...style
            }}
            data-email-component="container"
        >
            {children}
        </div>
    );
};

EmailContainer.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The children of this component.
     */
    children: PropTypes.node,

    /**
     * Inline styles for the container.
     */
    style: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default EmailContainer;
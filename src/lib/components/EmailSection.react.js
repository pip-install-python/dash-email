import React from 'react';
import PropTypes from 'prop-types';

/**
 * EmailSection groups related content together.
 */
const EmailSection = ({
    id,
    children,
    style = {},
    setProps
}) => {
    return (
        <div
            id={id}
            style={style}
            data-email-component="section"
        >
            {children}
        </div>
    );
};

EmailSection.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The children of this component.
     */
    children: PropTypes.node,

    /**
     * Inline styles for the section.
     */
    style: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default EmailSection;
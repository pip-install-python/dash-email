import React from 'react';
import PropTypes from 'prop-types';

/**
 * EmailHeading renders heading text (h1-h6).
 */
const EmailHeading = ({
    id,
    children,
    as_: Tag = 'h1',
    style = {},
    setProps
}) => {
    return (
        <Tag
            id={id}
            style={{
                margin: '16px 0',
                ...style
            }}
            data-email-component="heading"
        >
            {children}
        </Tag>
    );
};

EmailHeading.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The heading text content.
     */
    children: PropTypes.node,

    /**
     * The heading level (h1, h2, h3, h4, h5, h6).
     */
    as_: PropTypes.oneOf(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']),

    /**
     * Inline styles for the heading.
     */
    style: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default EmailHeading;
import React from 'react';
import PropTypes from 'prop-types';

/**
 * EmailColumn creates a column within an EmailRow.
 * Uses table cell for email client compatibility.
 */
const EmailColumn = ({
    id,
    children,
    style = {},
    setProps
}) => {
    return (
        <td
            id={id}
            style={{
                verticalAlign: 'top',
                ...style
            }}
            data-email-component="column"
        >
            {children}
        </td>
    );
};

EmailColumn.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The children of this component.
     */
    children: PropTypes.node,

    /**
     * Inline styles for the column.
     */
    style: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default EmailColumn;
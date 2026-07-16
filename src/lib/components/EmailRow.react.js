import React from 'react';
import PropTypes from 'prop-types';

/**
 * EmailRow creates a horizontal row for layout purposes.
 * Uses table-based layout for email client compatibility.
 */
const EmailRow = ({
    id,
    children,
    style = {},
    setProps
}) => {
    return (
        <table
            id={id}
            style={{
                width: '100%',
                borderCollapse: 'collapse',
                ...style
            }}
            data-email-component="row"
            cellPadding="0"
            cellSpacing="0"
            border="0"
        >
            <tbody>
                <tr>
                    {children}
                </tr>
            </tbody>
        </table>
    );
};

EmailRow.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The children of this component (typically EmailColumn components).
     */
    children: PropTypes.node,

    /**
     * Inline styles for the row.
     */
    style: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default EmailRow;
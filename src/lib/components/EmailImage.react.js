import React from 'react';
import PropTypes from 'prop-types';

/**
 * EmailImage renders an image in the email.
 */
const EmailImage = ({
    id,
    src,
    alt = '',
    width,
    height,
    style = {},
    setProps
}) => {
    return (
        <img
            id={id}
            src={src}
            alt={alt}
            width={width}
            height={height}
            style={{
                display: 'block',
                outline: 'none',
                border: 'none',
                textDecoration: 'none',
                ...style
            }}
            data-email-component="image"
        />
    );
};

EmailImage.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The image source URL. Should be an absolute URL for production.
     */
    src: PropTypes.string.isRequired,

    /**
     * Alternative text for the image.
     */
    alt: PropTypes.string,

    /**
     * The width of the image (number or string like "100%").
     */
    width: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),

    /**
     * The height of the image (number or string).
     */
    height: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),

    /**
     * Inline styles for the image.
     */
    style: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default EmailImage;
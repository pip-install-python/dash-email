import React from 'react';
import PropTypes from 'prop-types';

/**
 * EmailFont loads a custom font for use in the email.
 * In preview mode, this adds a style tag with @font-face.
 */
const EmailFont = ({
    id,
    fontFamily,
    fallbackFontFamily = 'Helvetica',
    webFont,
    fontStyle = 'normal',
    fontWeight = 400,
    setProps
}) => {
    // Generate @font-face CSS if webFont is provided
    const fontFaceCSS = webFont ? `
        @font-face {
            font-family: '${fontFamily}';
            font-style: ${fontStyle};
            font-weight: ${fontWeight};
            src: url('${webFont.url}') format('${webFont.format}');
        }
    ` : '';

    return (
        <style
            id={id}
            data-email-component="font"
            dangerouslySetInnerHTML={{ __html: fontFaceCSS }}
        />
    );
};

EmailFont.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The font family name.
     */
    fontFamily: PropTypes.string.isRequired,

    /**
     * Fallback font family if the web font fails to load.
     */
    fallbackFontFamily: PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.arrayOf(PropTypes.string)
    ]),

    /**
     * Web font configuration object with url and format properties.
     */
    webFont: PropTypes.shape({
        url: PropTypes.string.isRequired,
        format: PropTypes.string.isRequired
    }),

    /**
     * Font style (normal, italic).
     */
    fontStyle: PropTypes.string,

    /**
     * Font weight (400, 700, bold, etc.)
     */
    fontWeight: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default EmailFont;
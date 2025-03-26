import React, { forwardRef } from 'react';

const MultiSeriesLines = forwardRef<SVGGElement>(function MultiSeriesLines(props, ref) {
    return (
        <g
            ref={ref}
            className="lines-paths"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            {...props}
        />
    );
});

export default MultiSeriesLines;

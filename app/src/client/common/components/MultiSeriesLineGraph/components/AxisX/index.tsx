import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

function AxisX() {
    const gxRef = useRef<SVGGElement>(null);

    useEffect(() => {
        if (gxRef.current != null) {
            d3.select(gxRef.current).call(
                d3
                    .axisBottom(x)
                    .ticks(width / 80)
                    .tickSizeOuter(0),
            );
        }
    }, []);

    return <g ref={gxRef} transform={`translate(0, ${height - marginBottom})`} />;
}

export default AxisX;

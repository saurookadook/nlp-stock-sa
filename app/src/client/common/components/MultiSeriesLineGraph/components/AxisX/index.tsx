import React, { useContext, useEffect, useRef } from 'react';
import * as d3 from 'd3';

import { MSLGraphContext } from 'client/common/components/MultiSeriesLineGraph/constants';

function AxisX() {
    const stateContext = useContext(MSLGraphContext);
    const {
        graphConfig: { height, margins, width, xScale },
    } = stateContext;

    const gxRef = useRef<SVGGElement>(null);

    useEffect(() => {
        if (gxRef.current != null) {
            d3.select(gxRef.current).call(
                d3
                    .axisBottom(xScale)
                    .ticks(width / 80)
                    .tickSizeOuter(0),
            );
        }
    }, []);

    return <g ref={gxRef} transform={`translate(0, ${height - margins.bottom})`} />;
}

export default AxisX;

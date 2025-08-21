import React, { useContext, useEffect, useRef } from 'react';
import * as d3 from 'd3';

import { MSLGraphContext } from 'client/common/components/MultiSeriesLineGraph/constants';

function AxisY() {
    const stateContext = useContext(MSLGraphContext);
    const {
        graphConfig: { margins, width, yScale },
    } = stateContext;

    const gyRef = useRef<SVGGElement>(null);

    useEffect(() => {
        if (gyRef.current != null) {
            d3.select(gyRef.current)
                .call(d3.axisLeft(yScale))
                .call((g) => g.select('.domain').remove())
                .call((g) =>
                    g
                        .selectAll('.tick line')
                        .clone()
                        .attr('x2', width - margins.left - margins.right)
                        .attr('stroke-opacity', 0.1),
                )
                .call((g) =>
                    g
                        .append('text')
                        .attr('x', -margins.left)
                        .attr('y', 10)
                        .attr('fill', 'currentColor')
                        .attr('text-anchor', 'start')
                        .text('↑ Score change (%)'),
                );
        }
    }, []);

    return <g ref={gyRef} transform={`translate(${margins.left}, 0)`} />;
}

export default AxisY;

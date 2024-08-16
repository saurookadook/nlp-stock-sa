import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

function AxisY() {
    const gyRef = useRef<SVGGElement>(null);

    useEffect(() => {
        if (gyRef.current != null) {
            d3.select(gyRef.current)
                .call(d3.axisLeft(y))
                .call((g) => g.select('.domain').remove())
                .call((g) =>
                    g
                        .selectAll('.tick line')
                        .clone()
                        .attr('x2', width - marginLeft - marginRight)
                        .attr('stroke-opacity', 0.1),
                )
                .call((g) =>
                    g
                        .append('text')
                        .attr('x', -marginLeft)
                        .attr('y', 10)
                        .attr('fill', 'currentColor')
                        .attr('text-anchor', 'start')
                        .text('↑ Score change (%)'),
                );
        }
    }, []);

    return <g ref={gyRef} transform={`translate(${marginLeft}, 0)`} />;
}

export default AxisY;

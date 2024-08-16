import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

import type { SentimentAnalysesDataEntry, DispatchParams } from '@nlpssa-app-types/common/main';
import { AxisX, AxisY, MultiSeriesLines } from 'client/common/components/MultiSeriesLineGraph/components';
import { polarities, strokeColorByPolarity } from 'client/common/components/MultiSeriesLineGraph/constants';
import { buildPoints } from 'client/common/components/MultiSeriesLineGraph/utils';
import { StyledSVG } from './styled';

function Graph() {
    const svgRef = useRef<SVGSVGElement>(null);
    const linesPathsRef = useRef<SVGGElement>(null);
    const dotRef = useRef<SVGGElement>(null);

    const points = buildPoints({ data: sentimentAnalysesData, xFn: x, yFn: y });
    const groups = d3.rollup(
        points,
        (v) => Object.assign(v, { z: v[0][2] }),
        (d) => d[2],
    );

    const simpleLineGenerator = d3.line<[number, number]>();

    useEffect(() => {
        if (linesPathsRef.current != null) {
            d3.select(linesPathsRef.current)
                .selectAll('path')
                .data(groups.values())
                .join('path')
                .each(function (p, j) {
                    const path = d3.select(this);
                    const polarity = polarities[j];
                    console.log({ p, j, path, polarity });
                    path.classed('line-path', true)
                        .attr('aria-label', polarity)
                        .style('stroke', strokeColorByPolarity[polarity])
                        .attr('d', simpleLineGenerator as (data) => string);
                });
        }
    }, []);

    // When the pointer moves, find the closest point, update the interactive tip, and highlight
    // the corresponding line. Note: we don't actually use Voronoi here, since an exhaustive search
    // is fast enough.
    function pointermoved(event) {
        try {
            const [eventX, eventY] = d3.pointer(event);
            const i = Number(d3.leastIndex(points, ([x, y]) => Math.hypot(Number(x) - eventX, Number(y) - eventY)));
            const [x, y, k] = points[i];
            const paths = d3.select(linesPathsRef.current).selectAll('path');
            paths
                // @ts-expect-error: Not sure how to type this but it's correct
                .style('stroke', function ({ z }) {
                    const pathEl = d3.select(this).node() as SVGPathElement;
                    const polarityLabel = pathEl.getAttribute('aria-label') || '';
                    return z === k ? strokeColorByPolarity[polarityLabel] : '#dddddd';
                })
                // @ts-expect-error: Not sure how to type this but it's correct
                .filter(({ z }) => z === k)
                .raise();
            d3.select(dotRef.current) // force formatting
                .attr('transform', `translate(${x},${y})`)
                .select('text')
                .text(k);
            d3.select(svgRef.current)
                .property('value', sentimentAnalysesData[i])
                .dispatch('input', { bubbles: true } as DispatchParams);
        } catch (e) {
            console.groupCollapsed("ERROR: encountered in 'pointermoved' callback");
            console.error(e);
            console.groupEnd();
        }
    }

    function pointerentered() {
        try {
            d3.select(linesPathsRef.current).style('mix-blend-mode', null).style('stroke', '#ddd');
            d3.select(dotRef.current).attr('display', null);
        } catch (e) {
            console.groupCollapsed("ERROR: encountered in 'pointerentered' callback");
            console.error(e);
            console.groupEnd();
        }
    }

    function pointerleft() {
        try {
            const paths = d3.select(linesPathsRef.current).selectAll('path');
            paths.each(function () {
                const pathEl = d3.select(this);
                const polarityLabel = (pathEl.node() as SVGPathElement).getAttribute('aria-label') || '';
                pathEl.style('stroke', strokeColorByPolarity[polarityLabel]);
            });
            d3.select(dotRef.current).attr('display', 'none');
            d3.select(svgRef.current).dispatch('input', { bubbles: true } as DispatchParams);
        } catch (e) {
            console.groupCollapsed("ERROR: encountered in 'pointerleft' callback");
            console.error(e);
            console.groupEnd();
        }
    }

    return (
        <StyledSVG
            ref={svgRef}
            width={width}
            height={height + legendItemSize + legendSpacer}
            viewBox={`0 0 ${width} ${height}`}
            onPointerEnter={pointerentered}
            onPointerMove={pointermoved}
            onPointerLeave={pointerleft}
            onTouchStart={(event) => event.preventDefault()}
        >
            <AxisX />
            <AxisY />
            <MultiSeriesLines ref={linesPathsRef} />
        </StyledSVG>
    );
}

export default Graph;

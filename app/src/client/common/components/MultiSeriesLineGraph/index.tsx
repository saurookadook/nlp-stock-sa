import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

import type { SentimentAnalysesDataEntry, DispatchParams } from '@nlpssa-app-types/common/main';
import Legend from 'client/common/components/MultiSeriesLineGraph/Legend';
import { polarities, strokeColorByPolarity } from 'client/common/components/MultiSeriesLineGraph/constants';
import { createXScale, createYScale, buildPoints } from 'client/common/components/MultiSeriesLineGraph/utils';
import { StyledGraphWrapper, StyledSVG } from 'client/common/components/MultiSeriesLineGraph/styled';

// 640 / 16 = 40
// 400 / 16 = 25
// -- 40 / 25 = 1.6
function MultiSeriesLineGraph({
    sentimentAnalysesData,
    legendItemSize = 20,
    legendSpacer = 16,
    width = 768,
    height = 480,
    marginTop = 20,
    marginRight = 20,
    marginBottom = 30,
    marginLeft = 40,
}: React.PropsWithChildren<{
    sentimentAnalysesData: SentimentAnalysesDataEntry[];
    legendItemSize?: number;
    legendSpacer?: number;
    width?: number;
    height?: number;
    marginTop?: number;
    marginRight?: number;
    marginBottom?: number;
    marginLeft?: number;
}>) {
    const svgRef = useRef<SVGSVGElement>(null);
    const gxRef = useRef<SVGGElement>(null);
    const gyRef = useRef<SVGGElement>(null);
    const linesPathsRef = useRef<SVGGElement>(null);
    const dotRef = useRef<SVGGElement>(null);

    const x = createXScale({
        data: sentimentAnalysesData,
        marginLeft,
        marginRight,
        width,
    });

    const y = createYScale({
        boundLower: -1,
        boundUpper: 1,
        height,
        marginBottom,
        marginTop,
    });

    const points = buildPoints({ data: sentimentAnalysesData, xFn: x, yFn: y });

    const groups = d3.rollup(
        points,
        (v) => Object.assign(v, { z: v[0][2] }),
        (d) => d[2],
    );

    // const lineGenerator = d3
    //     .line<D3Point>()
    //     .x((d) => x(d[0]))
    //     .y((d) => y(d[1]));

    const simpleLineGenerator = d3.line<[number, number]>();

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

    return (
        <StyledGraphWrapper>
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
                <g ref={gxRef} transform={`translate(0, ${height - marginBottom})`} />
                <g ref={gyRef} transform={`translate(${marginLeft}, 0)`} />
                <g
                    ref={linesPathsRef}
                    className="lines-paths"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                />
                <g ref={dotRef} display="none" fill="white" stroke="currentColor" strokeWidth="1.5">
                    <circle r="2.5" />
                    <text textAnchor="middle" y={-8} r="2.5" />
                </g>
                <Legend height={height} legendItemSize={legendItemSize} legendSpacer={legendSpacer} />
            </StyledSVG>
        </StyledGraphWrapper>
    );
}

export default MultiSeriesLineGraph;

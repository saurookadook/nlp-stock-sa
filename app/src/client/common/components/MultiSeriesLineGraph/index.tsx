import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

import type { SentimentAnalysesDataEntry } from '@nlpssa-app-types/common/main';
import Legend from 'client/common/components/MultiSeriesLineGraph/Legend';
import { polarities, strokeColorByPolarity } from 'client/common/components/MultiSeriesLineGraph/constants';
import { StyledGraphWrapper, StyledSVG } from 'client/common/components/MultiSeriesLineGraph/styled';

type DispatchParams = d3.CustomEventParameters & { bubble?: boolean };

type D3Point = [number, number, string];

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
    const gx = useRef<SVGGElement>(null);
    const gy = useRef<SVGGElement>(null);
    const linesPathsRef = useRef<SVGGElement>(null);
    const dot = useRef<SVGGElement>(null);

    const dateValue = (d: SentimentAnalysesDataEntry) =>
        (d.source?.data?.last_updated_date || d.source?.data?.published_date) as Date;

    const x = d3
        .scaleUtc()
        .domain(d3.extent(sentimentAnalysesData, dateValue) as [Date, Date])
        .range([marginLeft, width - marginRight]);

    const y = d3
        .scaleLinear()
        .domain([-1, 1])
        .nice()
        .range([height - marginBottom, marginTop]);

    const points = sentimentAnalysesData.reduce(function (acc: D3Point[], d: SentimentAnalysesDataEntry) {
        acc.push([
            x(d.source!.data!.last_updated_date as Date),
            y(d.output.compound),
            `${d.quoteStockSymbol}: Compound score`,
        ]);
        acc.push([
            x(d.source!.data!.last_updated_date as Date),
            y(d.output.neg),
            `${d.quoteStockSymbol}: Negative score`,
        ]);
        acc.push([
            x(d.source!.data!.last_updated_date as Date),
            y(d.output.neu),
            `${d.quoteStockSymbol}: Neutral score`,
        ]);
        acc.push([
            x(d.source!.data!.last_updated_date as Date),
            y(d.output.pos),
            `${d.quoteStockSymbol}: Positive score`,
        ]);

        return acc;
    }, []);

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

    useEffect(() => {
        if (linesPathsRef.current != null) {
            d3.select(linesPathsRef.current)
                .append('g')
                .classed('lines-paths', true)
                .attr('fill', 'none')
                .attr('stroke-width', 1.5)
                .attr('stroke-linejoin', 'round')
                .attr('stroke-linecap', 'round')
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
                        // .attr('d', lineGenerator as (data) => string);
                        // @ts-expect-error: testing
                        .attr('d', simpleLineGenerator);
                    // debugger;
                });
        }
    }, []);

    // When the pointer moves, find the closest point, update the interactive tip, and highlight
    // the corresponding line. Note: we don't actually use Voronoi here, since an exhaustive search
    // is fast enough.
    function pointermoved(event) {
        // console.groupCollapsed('pointermoved callback - event');
        console.log(event, points);
        // console.groupEnd();
        try {
            const [eventX, eventY] = d3.pointer(event);
            const i = Number(d3.leastIndex(points, ([x, y]) => Math.hypot(Number(x) - eventX, Number(y) - eventY)));
            const [x, y, k] = points[i];
            // TODO: fix weird type error
            // console.groupCollapsed('pointermoved callback - other vars');
            console.log({ eventX, eventY, i, x, y, k });
            // console.groupEnd();
            const paths = d3.select(svgRef.current).selectAll('path.line-path');
            // console.log({ paths });
            paths.each(function (d, i, nodes) {
                const el = nodes[i] as SVGPathElement;
                const polarityLabel = el.getAttribute('aria-label') || '';
                // console.log({ el, polarityForNode: polarities[i], polarityLabel });
                if (k.indexOf(polarityLabel) > -1) {
                    d3.select(el).raise();
                } else {
                    el.style.stroke = '#dddddd';
                }
            });
            d3.select(dot.current) // force formatting
                .attr('transform', `translate(${x},${y})`)
                .select('text')
                .text(k);
            d3.select(svgRef.current)
                .property('value', sentimentAnalysesData[i])
                .dispatch('input', { bubbles: true } as DispatchParams);
        } catch (e) {
            // console.groupCollapsed('ERROR: pointermoved');
            console.error(e);
            // console.groupEnd();
        }
    }

    function pointerentered(event) {
        console.groupCollapsed('pointerentered callback');
        console.log({ event });
        console.groupEnd();
        d3.select(linesPathsRef.current).style('mix-blend-mode', null).style('stroke', '#ddd');
        d3.select(dot.current).attr('display', null);
    }

    function pointerleft() {
        const paths = d3.select(svgRef.current).selectAll('path.line-path');
        // console.log({ paths });
        paths.each(function (d, i, nodes) {
            const el = nodes[i] as SVGPathElement;
            const polarityLabel = el.getAttribute('aria-label') || '';
            // console.log({ el, polarityForNode: polarities[i], polarityLabel });
            el.style.stroke = strokeColorByPolarity[polarityLabel];
        });
        d3.select(dot.current).attr('display', 'none');
        // TODO: fix weird type error
        // d3.select(svgRef.current).node().value = null;
        d3.select(svgRef.current).dispatch('input', { bubbles: true } as DispatchParams);
    }

    useEffect(() => {
        if (gx.current != null) {
            d3.select(gx.current).call(
                d3
                    .axisBottom(x)
                    .ticks(width / 80)
                    .tickSizeOuter(0),
            );
        }
    }, []);

    useEffect(() => {
        if (gy.current != null) {
            d3.select(gy.current)
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
                <g ref={gx} transform={`translate(0,${height - marginBottom})`} />
                <g ref={gy} transform={`translate(${marginLeft},0)`} />
                <g ref={linesPathsRef} className="lines-paths" />
                <g ref={dot} display="none" fill="white" stroke="currentColor" strokeWidth="1.5">
                    <circle r="2.5" />
                    <text textAnchor="middle" y={-8} r="2.5" />
                </g>
                <Legend height={height} legendItemSize={legendItemSize} legendSpacer={legendSpacer} />
            </StyledSVG>
        </StyledGraphWrapper>
    );
}

export default MultiSeriesLineGraph;

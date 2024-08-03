import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import styled from '@emotion/styled';
import { Flex } from '@chakra-ui/react';

import type { SentimentAnalysesDataEntry } from '@nlpssa-app-types/common/main';
import Legend from './Legend';

const StyledGraphWrapper = styled(Flex)`
    flex-direction: row;
`;

const StyledSVG = styled.svg`
    font: 10px sans-serif;
    height: auto;
    max-width: 100%;
    overflow: visible;
`;

const polarities = ['Compound', 'Negative', 'Neutral', 'Positive'];

const strokeColorByPolarity = {
    Compound: 'steelblue',
    Negative: 'red',
    Neutral: 'orange',
    Positive: 'green',
};

type DispatchParams = d3.CustomEventParameters & { bubble?: boolean };

type D3Point = [Date, number, string];

type PointsByPolarityType = {
    Compound: D3Point[];
    Negative: D3Point[];
    Neutral: D3Point[];
    Positive: D3Point[];
};

type LinesPathsRef = d3.Selection<SVGPathElement | d3.BaseType, D3Point[] & { z: string }, SVGGElement, unknown> & {
    _groups: [SVGPathElement, number][];
};

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
    // const linesPaths = useRef<SVGGElement>(null);
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
            d.source!.data!.last_updated_date as Date,
            d.output.compound,
            `${d.quoteStockSymbol}: Compound score`,
        ]);
        acc.push([d.source!.data!.last_updated_date as Date, d.output.neg, `${d.quoteStockSymbol}: Negative score`]);
        acc.push([d.source!.data!.last_updated_date as Date, d.output.neu, `${d.quoteStockSymbol}: Neutral score`]);
        acc.push([d.source!.data!.last_updated_date as Date, d.output.pos, `${d.quoteStockSymbol}: Positive score`]);

        return acc;
    }, []);

    const groups = d3.rollup(
        points,
        (v) => Object.assign(v, { z: v[0][2] }),
        (d) => d[2],
    );

    const compoundPoints = sentimentAnalysesData.reduce(
        function (acc: PointsByPolarityType, d: SentimentAnalysesDataEntry) {
            // could probably remove this at some point...
            if (d.source != null) {
                acc.Compound.push([
                    d.source!.data!.last_updated_date as Date,
                    d.output.compound,
                    `${d.quoteStockSymbol}: Compound score`,
                ]);
                // acc.Compound.push([x(dateValue(d)), y(d.output.compound), `${d.quoteStockSymbol}: Compound score`]);
                acc.Negative.push([
                    d.source!.data!.last_updated_date as Date,
                    d.output.neg,
                    `${d.quoteStockSymbol}: Negative score`,
                ]);
                // acc.Negative.push([x(dateValue(d)), y(d.output.neg), `${d.quoteStockSymbol}: Negative score`]);
                acc.Neutral.push([
                    d.source!.data!.last_updated_date as Date,
                    d.output.neu,
                    `${d.quoteStockSymbol}: Neutral score`,
                ]);
                // acc.Neutral.push([x(dateValue(d)), y(d.output.neu), `${d.quoteStockSymbol}: Neutral score`]);
                acc.Positive.push([
                    d.source!.data!.last_updated_date as Date,
                    d.output.pos,
                    `${d.quoteStockSymbol}: Positive score`,
                ]);
                // acc.Positive.push([x(dateValue(d)), y(d.output.pos), `${d.quoteStockSymbol}: Positive score`]);
            }
            return acc;
        },
        {
            Compound: [],
            Negative: [],
            Neutral: [],
            Positive: [],
        },
    );

    const lineGenerator = d3
        .line<D3Point>()
        .x((d) => x(d[0]))
        .y((d) => y(d[1]));

    let linesPaths;

    useEffect(() => {
        if (svgRef.current) {
            linesPaths = d3
                .select(svgRef.current)
                .append('g')
                .classed('lines-paths', true)
                .attr('fill', 'none')
                .attr('stroke-width', 1.5)
                .attr('stroke-linejoin', 'round')
                .attr('stroke-linecap', 'round')
                .selectAll('path')
                .data(groups.values())
                .join('path');

            linesPaths._groups[0].map(function (path: SVGPathElement, i: number) {
                const polarity = polarities[i];
                return d3
                    .select(path)
                    .classed('line-path', true)
                    .attr('aria-label', polarity)
                    .style('stroke', strokeColorByPolarity[polarity])
                    .attr('d', lineGenerator as (data) => string);
                // .attr('d', lineGenerator(compoundPoints[polarity]) as string)
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
        d3.select(linesPaths.current).style('mix-blend-mode', null).style('stroke', '#ddd');
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
                {/* <g ref={linesPathsRef} className="lines-paths" /> */}
                {/* {polarities.map((pol, i) => (
                    <path
                        key={`polarity-score-line-${i}`}
                        className="line-path"
                        fill="none"
                        stroke={strokeColorByPolarity[pol]}
                        strokeWidth="1.5"
                        d={lineGenerator(compoundPoints[pol]) as string}
                    />
                ))} */}
                <g ref={dot} display="none" fill="white" stroke="currentColor" strokeWidth="1.5">
                    {sentimentAnalysesData.map((d, i) => (
                        // cx={x(i)} cy={y(d)}
                        <>
                            <circle key={`circle-${i}`} r="2.5" />
                            <text key={`sa-text-${i}`} textAnchor="middle" y={-8} r="2.5" />
                        </>
                    ))}
                </g>
                <Legend height={height} legendItemSize={legendItemSize} legendSpacer={legendSpacer} />
            </StyledSVG>
        </StyledGraphWrapper>
    );
}

export default MultiSeriesLineGraph;

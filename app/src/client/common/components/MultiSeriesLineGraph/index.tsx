import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import styled from '@emotion/styled';

import type { SentimentAnalysesDataEntry } from '@nlpssa-app-types/common/main';

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
    Neutral: 'black',
    Positive: 'green',
};

// type DispatchParams = d3.CustomEventParameters & { bubble?: boolean };

// type D3Point = [number, number, string];
type D3Point = [Date, number, string];

type PointsByPolarityType = {
    Compound: D3Point[];
    Negative: D3Point[];
    Neutral: D3Point[];
    Positive: D3Point[];
};

/**
 * @description TODO: this thing is doing way too much stuff at the moment; \
 * eventually, it should _only_ be sorting by last_update_date or published_date :)
 * @param a
 * @param b
 */
function compareByDateCallback(a: SentimentAnalysesDataEntry, b: SentimentAnalysesDataEntry) {
    const aField = a.source!.data!.last_updated_date as Date;
    const bField = b.source!.data!.last_updated_date as Date;
    // let aField: Date = new Date(a.source!.data!.created_at);
    // let bField: Date = new Date(b.source!.data!.created_at);

    // if (dateFieldIsValid(a.source?.data?.last_updated_date) && dateFieldIsValid(b.source?.data?.last_updated_date)) {
    //     aField = a.source!.data!.last_updated_date as Date;
    //     bField = b.source!.data!.last_updated_date as Date;
    // } else if (dateFieldIsValid(a.source?.data?.published_date) && dateFieldIsValid(b.source?.data?.published_date)) {
    //     aField = a.source!.data!.published_date as Date;
    //     bField = b.source!.data!.published_date as Date;
    // }

    return aField == bField ? 0 : Number(aField > bField) - Number(aField < bField);
}

function dateFieldIsValid(dateField: unknown) {
    return dateField != null && typeof dateField === 'string' && dateField !== '';
}

// 640 / 16 = 40
// 400 / 16 = 25
// -- 40 / 25 = 1.6
function MultiSeriesLineGraph({
    data,
    width = 768,
    height = 480,
    marginTop = 20,
    marginRight = 20,
    marginBottom = 30,
    marginLeft = 40,
}: React.PropsWithChildren<{
    data: SentimentAnalysesDataEntry[];
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

    // TODO: the creation of the date fields here is only temporary; that kind of
    // normalization should probably be done in the reducer
    const sortedDataWithSources = data
        .filter((d) => d.source != null)
        .map(function (d) {
            if (dateFieldIsValid(d.source?.data?.last_updated_date)) {
                d.source!.data!.last_updated_date = new Date(d.source!.data!.last_updated_date as string);
            }
            if (dateFieldIsValid(d.source?.data?.published_date)) {
                d.source!.data!.published_date = new Date(d.source!.data!.published_date as string);
            }
            return d;
        })
        .sort(compareByDateCallback);

    const dateValue = (d: SentimentAnalysesDataEntry) =>
        (d.source?.data?.last_updated_date || d.source?.data?.published_date) as Date;

    const x = d3
        .scaleUtc()
        .domain(d3.extent(sortedDataWithSources, dateValue) as [Date, Date])
        .range([marginLeft, width - marginRight]);

    const y = d3
        .scaleLinear()
        .domain([-1, 1])
        .nice()
        .range([height - marginBottom, marginTop]);

    const compoundPoints = sortedDataWithSources.reduce(
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

    // When the pointer moves, find the closest point, update the interactive tip, and highlight
    // the corresponding line. Note: we don't actually use Voronoi here, since an exhaustive search
    // is fast enough.
    // function pointermoved(event) {
    //     const [xm, ym] = d3.pointer(event);
    //     const i = Number(d3.leastIndex(compoundPoints, ([x, y]) => Math.hypot(Number(x) - xm, Number(y) - ym)));
    //     const [x, y, k] = compoundPoints[i];
    //     // TODO: fix weird type error
    //     // d3.select(linesPaths.current).style("stroke", ({ z }) => z === k ? null : "#ddd").filter(({ z }) => z === k).raise();
    //     const dotEl = d3.select(dot.current);
    //     dotEl.attr('transform', `translate(${x},${y})`);
    //     dotEl.select('text').text(k);
    //     d3.select(svgRef.current)
    //         .property('value', data[i])
    //         .dispatch('input', { bubbles: true } as DispatchParams);
    // }

    // function pointerentered() {
    //     d3.select(linesPaths.current).style('mix-blend-mode', null).style('stroke', '#ddd');
    //     d3.select(dot.current).attr('display', null);
    // }

    // function pointerleft() {
    //     d3.select(linesPaths.current).style('mix-blend-mode', 'multiply').style('stroke', null);
    //     d3.select(dot.current).attr('display', 'none');
    //     // TODO: fix weird type error
    //     // d3.select(svgRef.current).node().value = null;
    //     d3.select(svgRef.current).dispatch('input', { bubbles: true } as DispatchParams);
    // }

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
        <StyledSVG
            ref={svgRef}
            width={width}
            height={height}
            viewBox={`0 0 ${width} ${height}`}
            // onPointerEnter={pointerentered}
            // onPointerMove={pointermoved}
            // onPointerLeave={pointerleft}
            onTouchStart={(event) => event.preventDefault()}
        >
            <g ref={gx} transform={`translate(0,${height - marginBottom})`} />
            <g ref={gy} transform={`translate(${marginLeft},0)`} />
            {polarities.map((pol, i) => (
                <path
                    key={`polarity-score-line-${i}`}
                    fill="none"
                    stroke={strokeColorByPolarity[pol]}
                    strokeWidth="1.5"
                    d={lineGenerator(compoundPoints[pol]) as string}
                />
            ))}
            <g ref={dot} display="none" fill="white" stroke="currentColor" strokeWidth="1.5">
                {data.map((d, i) => (
                    // cx={x(i)} cy={y(d)}
                    <circle key={`circle-${i}`} r="2.5" />
                ))}
                {data.map((d, i) => (
                    <text key={i} textAnchor="middle" y={y(d.output.compound)} r="2.5" />
                ))}
            </g>
        </StyledSVG>
    );
}

export default MultiSeriesLineGraph;

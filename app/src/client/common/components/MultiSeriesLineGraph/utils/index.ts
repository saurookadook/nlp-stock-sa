import * as d3 from 'd3';

import type {
    SentimentAnalysesDataEntry, // force formatting
    D3Point,
    AxisScaleFnX,
    AxisScaleFnY,
} from '@nlpssa-app-types/common/main';

function safeGetDateValue(d: SentimentAnalysesDataEntry): Date {
    const resolvedDateValue = d.source?.data?.last_updated_date || d.source?.data?.published_date;
    // TODO: fix types so there's no need for the `new Date()` fallback?
    return resolvedDateValue != null ? new Date(resolvedDateValue) : new Date();
}

function createXScale({
    data,
    marginLeft,
    marginRight,
    width,
    dateGetterFn = safeGetDateValue,
}: {
    data: SentimentAnalysesDataEntry[];
    marginLeft: number;
    marginRight: number;
    width: number;
    dateGetterFn?: (d: SentimentAnalysesDataEntry) => Date;
}): AxisScaleFnX {
    return d3
        .scaleUtc()
        .domain(d3.extent(data, dateGetterFn) as [Date, Date])
        .range([marginLeft, width - marginRight]);
}

function createYScale({
    boundLower,
    boundUpper,
    height,
    marginBottom,
    marginTop,
}: {
    boundLower: number;
    boundUpper: number;
    height: number;
    marginBottom: number;
    marginTop: number;
}): AxisScaleFnY {
    return d3
        .scaleLinear()
        .domain([boundLower, boundUpper])
        .nice()
        .range([height - marginBottom, marginTop]);
}

function buildPoints({
    data, // force formatting
    xFn,
    yFn,
}: {
    data: SentimentAnalysesDataEntry[];
    xFn: AxisScaleFnX;
    yFn: AxisScaleFnY;
}) {
    return data.reduce(function (acc: D3Point[], d: SentimentAnalysesDataEntry) {
        acc.push([xFn(safeGetDateValue(d)), yFn(d.output.compound), `${d.quoteStockSymbol}: Compound score`]);
        acc.push([xFn(safeGetDateValue(d)), yFn(d.output.neg), `${d.quoteStockSymbol}: Negative score`]);
        acc.push([xFn(safeGetDateValue(d)), yFn(d.output.neu), `${d.quoteStockSymbol}: Neutral score`]);
        acc.push([xFn(safeGetDateValue(d)), yFn(d.output.pos), `${d.quoteStockSymbol}: Positive score`]);

        return acc;
    }, []);
}

export { createXScale, createYScale, buildPoints, safeGetDateValue };

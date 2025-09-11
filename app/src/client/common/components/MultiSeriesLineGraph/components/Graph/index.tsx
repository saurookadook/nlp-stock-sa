import React, { useContext, useEffect, useRef } from 'react';
import * as d3 from 'd3';

import type { DispatchParams } from '@nlpssa-app-types/common/main';
import {
  AxisX,
  AxisY,
  Legend,
  MultiSeriesLines,
} from 'client/common/components/MultiSeriesLineGraph/components';
import {
  MSLGraphContext,
  polarities,
  strokeColorByPolarity,
} from 'client/common/components/MultiSeriesLineGraph/constants';
import { buildPoints } from 'client/common/components/MultiSeriesLineGraph/utils';
import { StyledSVG } from './styled';

// @ts-expect-error: I don't plan on this being a permament thing lol
window.MULTI_SERIES_GRAPH_LOGGING_ENABLED = Boolean(
  window.localStorage.getItem('MULTI_SERIES_GRAPH_LOGGING_ENABLED'),
);

function Graph() {
  const stateContext = useContext(MSLGraphContext);
  const {
    graphConfig: { data, height, legend, width, xScale, yScale },
  } = stateContext;

  const svgRef = useRef<SVGSVGElement>(null);
  const linesPathsRef = useRef<SVGGElement>(null);
  const dotRef = useRef<SVGGElement>(null);

  const points = buildPoints({ data: data, xFn: xScale, yFn: yScale });
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

          logLocal({ p, j, path, polarity });

          path
            .classed('line-path', true)
            .attr('aria-label', polarity)
            .style('stroke', strokeColorByPolarity[polarity].hex)
            .attr('d', simpleLineGenerator as (data) => string);
        });
    }
  }, []);

  // When the pointer moves, find the closest point, update the interactive tip,
  // and highlight the corresponding line.
  //
  // NOTE:
  // we don't actually use Voronoi here, since an exhaustive search is fast enough.
  function pointermoved(event) {
    try {
      const [eventX, eventY] = d3.pointer(event);
      const i = Number(
        d3.leastIndex(points, ([x, y]) =>
          Math.hypot(Number(x) - eventX, Number(y) - eventY),
        ),
      );
      const [x, y, labelText, saID] = points[i];

      logLocal(
        JSON.parse(
          JSON.stringify({
            eventName: 'pointermoved',
            eventX,
            eventY,
            i,
            x,
            y,
            labelText,
            saID,
          }),
        ),
      );

      const paths = d3.select(linesPathsRef.current).selectAll('path');
      paths
        // @ts-expect-error: Not sure how to type this but it's correct
        .style('stroke', function ({ z }) {
          const pathEl = d3.select(this).node() as SVGPathElement;
          const polarityLabel = pathEl.getAttribute('aria-label') || '';

          return z === labelText // force formatting
            ? strokeColorByPolarity[polarityLabel].hex
            : '#dddddd';
        })
        // @ts-expect-error: Not sure how to type this but it's correct
        .filter(({ z }) => z === labelText)
        .raise();
      d3.select(dotRef.current) // force formatting
        .attr('transform', `translate(${x},${y})`)
        .select('text')
        .text(labelText);
      d3.select(svgRef.current)
        .property('value', data[i])
        .dispatch('input', { bubbles: true } as DispatchParams);
    } catch (e) {
      console.groupCollapsed(errorGroupLabelFactory(pointermoved.name));
      console.error(e);
      console.groupEnd();
    }
  }

  function pointerentered() {
    try {
      d3.select(linesPathsRef.current)
        .style('mix-blend-mode', null)
        .style('stroke', '#ddd');
      d3.select(dotRef.current).attr('display', null);
    } catch (e) {
      console.groupCollapsed(errorGroupLabelFactory(pointerentered.name));
      console.error(e);
      console.groupEnd();
    }
  }

  function pointerleft() {
    try {
      const paths = d3.select(linesPathsRef.current).selectAll('path');
      paths.each(function () {
        const pathEl = d3.select(this);
        const polarityLabel =
          (pathEl.node() as SVGPathElement).getAttribute('aria-label') || '';

        pathEl.style('stroke', strokeColorByPolarity[polarityLabel].hex);
      });
      d3.select(dotRef.current).attr('display', 'none');
      d3.select(svgRef.current).dispatch('input', { bubbles: true } as DispatchParams);
    } catch (e) {
      console.groupCollapsed(errorGroupLabelFactory(pointerleft.name));
      console.error(e);
      console.groupEnd();
    }
  }

  return (
    <StyledSVG
      ref={svgRef}
      width={width}
      height={height + legend.itemSize + legend.spacer}
      viewBox={`0 0 ${width} ${height}`}
      onPointerEnter={pointerentered}
      onPointerMove={pointermoved}
      onPointerLeave={pointerleft}
      onTouchStart={(event) => event.preventDefault()}
    >
      <AxisX />

      <AxisY />

      <MultiSeriesLines ref={linesPathsRef} />

      <g
        ref={dotRef}
        display="none"
        fill="white"
        stroke="currentColor"
        strokeWidth="1.5"
      >
        <circle r="2.5" />
        <text textAnchor="middle" y={-8} r="2.5" />
      </g>

      <Legend />
    </StyledSVG>
  );
}

function errorGroupLabelFactory(fnName: string) {
  return `ERROR: encountered in '${fnName}' callback`;
}

function logLocal(...args: any[]) {
  // @ts-expect-error: I don't plan on this being a permament thing lol
  if (window.MULTI_SERIES_GRAPH_LOGGING_ENABLED) {
    console.log(...args);
  }
}

export default Graph;

import React from 'react';

import { strokeColorByPolarity } from 'client/common/components/MultiSeriesLineGraph/constants';

function Legend({
    height,
    legendItemSize,
    legendSpacer,
}: {
    height: number;
    legendItemSize: number;
    legendSpacer: number;
}) {
    return (
        <g id="legend">
            {Object.entries(strokeColorByPolarity).map(([key, val], i) => {
                return (
                    <React.Fragment key={`legend-item-${i}`}>
                        <rect
                            x={100 + i * 100}
                            y={height - legendItemSize + legendSpacer}
                            fill={val}
                            height={legendItemSize}
                            width={legendItemSize}
                        />
                        <text
                            x={100 + i * 100 + legendItemSize + 5}
                            y={height + legendSpacer / 2}
                            alignmentBaseline="middle"
                            fill={val}
                            textAnchor="left"
                        >
                            {key}
                        </text>
                    </React.Fragment>
                );
            })}
        </g>
    );
}

export default Legend;

import React, { useContext } from 'react';

import { strokeColorByPolarity, MSLGraphContext } from 'client/common/components/MultiSeriesLineGraph/constants';

function Legend() {
    const stateContext = useContext(MSLGraphContext);
    const {
        graphConfig: { height, legend },
    } = stateContext;

    return (
        <g id="legend">
            {Object.entries(strokeColorByPolarity).map(([key, val], i) => {
                return (
                    <React.Fragment key={`legend-item-${i}`}>
                        <rect
                            x={100 + i * 100}
                            y={height - legend.itemSize + legend.spacer}
                            fill={val}
                            height={legend.itemSize}
                            width={legend.itemSize}
                        />
                        <text
                            x={100 + i * 100 + legend.itemSize + 5}
                            y={height + legend.spacer / 2}
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

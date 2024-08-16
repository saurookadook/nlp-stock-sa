import React, { useState } from 'react';

import type { SentimentAnalysesDataEntry, MSLGraphConfig } from '@nlpssa-app-types/common/main';
import { Graph } from 'client/common/components/MultiSeriesLineGraph/components';
import { MSLGraphContext, getMSLGraphConfig } from 'client/common/components/MultiSeriesLineGraph/constants';
import { StyledGraphWrapper } from './styled';

// 640 / 16 = 40
// 400 / 16 = 25
// -- 40 / 25 = 1.6
function MultiSeriesLineGraph({
    sentimentAnalysesData, // force formatting
}: React.PropsWithChildren<{
    sentimentAnalysesData: SentimentAnalysesDataEntry[];
}>) {
    const [graphConfig, setGraphConfig] = useState<MSLGraphConfig>(
        getMSLGraphConfig({ forFullSize: true, data: sentimentAnalysesData }),
    );

    // const x = createXScale({
    //     data: sentimentAnalysesData,
    //     marginLeft,
    //     marginRight,
    //     width,
    // });

    // const y = createYScale({
    //     boundLower: -1,
    //     boundUpper: 1,
    //     height,
    //     marginBottom,
    //     marginTop,
    // });

    // const lineGenerator = d3
    //     .line<D3Point>()
    //     .x((d) => x(d[0]))
    //     .y((d) => y(d[1]));

    return (
        <StyledGraphWrapper>
            <MSLGraphContext.Provider
                value={{
                    graphConfig,
                    setGraphConfig,
                }}
            >
                <Graph />
            </MSLGraphContext.Provider>
        </StyledGraphWrapper>
    );
}

export default MultiSeriesLineGraph;

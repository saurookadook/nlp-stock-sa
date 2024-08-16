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

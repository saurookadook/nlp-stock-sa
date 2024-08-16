import { createContext } from 'react';

import type { MSLGraphConfig, MSLGraphContext, SentimentAnalysesDataEntry } from '@nlpssa-app-types/common/main';
import { createXScale, createYScale } from 'client/common/components/MultiSeriesLineGraph/utils';

const polarities = ['Compound', 'Negative', 'Neutral', 'Positive'];

const strokeColorByPolarity = {
    Compound: 'steelblue',
    Negative: 'red',
    Neutral: 'orange',
    Positive: 'green',
};

/** MSL === Multi-Series Line */
const MSLGraphContext = createContext<MSLGraphContext>({
    graphConfig: getMSLGraphConfig({ forFullSize: true }),
    setGraphConfig: (config) => config,
});

function getMSLGraphConfig({
    forFullSize,
    data = [],
    // height = 0,
    // width = 0, // force formatting
}: {
    forFullSize: boolean;
    data?: SentimentAnalysesDataEntry[];
    // height?: number;
    // width?: number;
}): MSLGraphConfig {
    const commonSettings = {
        data: data,
        legend: {
            itemSize: 20,
            spacer: 16,
        },
    };

    const config = forFullSize
        ? {
              ...commonSettings,
              height: 480,
              margins: {
                  top: 20,
                  right: 20,
                  bottom: 30,
                  left: 40,
              },
              width: 768,
          }
        : {
              // TODO: revisit these values lol
              ...commonSettings,
              height: 240,
              margins: {
                  top: 10,
                  right: 10,
                  bottom: 15,
                  left: 20,
              },
              width: 384,
          };

    return {
        ...config,
        xScale: createXScale({
            data: config.data,
            marginLeft: config.margins.left,
            marginRight: config.margins.right,
            width: config.width,
        }),
        yScale: createYScale({
            boundLower: -1,
            boundUpper: 1,
            height: config.height,
            marginTop: config.margins.top,
            marginBottom: config.margins.bottom,
        }),
    };
}

export {
    polarities, // force formatting
    strokeColorByPolarity,
    MSLGraphContext,
    getMSLGraphConfig,
};

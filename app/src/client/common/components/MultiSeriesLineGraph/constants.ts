import { createContext } from 'react';

import type {
  MSLGraphConfig,
  MSLGraphContext,
  SentimentAnalysesDataEntry,
} from '@nlpssa-app-types/common/main';
import {
  createXScale,
  createYScale,
} from 'client/common/components/MultiSeriesLineGraph/utils';

const strokeColorByPolarity = {
  Compound: {
    hex: '#4682b4',
    name: 'steelblue',
    rgbWeights: '70 130 180',
  },
  Negative: {
    hex: '#ff0000',
    name: 'red',
    rgbWeights: '255 0 0',
  },
  Neutral: {
    hex: '#ffa500',
    name: 'orange',
    rgbWeights: '255 165 0',
  },
  Positive: {
    hex: '#008000',
    name: 'green',
    rgbWeights: '0 128 0',
  },
};

const polarities = Object.keys(strokeColorByPolarity);

/** MSL === Multi-Series Line */
const MSLGraphContext = createContext<MSLGraphContext>({
  graphConfig: getMSLGraphConfig({ forFullSize: true }),
  setGraphConfig: (config) => config,
});

function getMSLGraphConfig({
  forFullSize,
  data = [],
  // height = 0,
  width = 768, // force formatting
}: {
  forFullSize: boolean;
  data?: SentimentAnalysesDataEntry[];
  // height?: number;
  width?: number;
}): MSLGraphConfig {
  const commonSettings = {
    // TODO: should maybe do something more with this value...?
    initialWidth: width,
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
        width: commonSettings.initialWidth,
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
  MSLGraphContext,
  getMSLGraphConfig,
  polarities, // force formatting
  strokeColorByPolarity,
};

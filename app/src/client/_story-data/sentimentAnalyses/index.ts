import AMD from './AMD';
import INDO from './INDO';
import KOS from './KOS';
import NTDOF from './NTDOF';
import SHOP from './SHOP';
import TSLA from './TSLA';

import { SentimentAnalysesBySlugApiData } from '@nlpssa-app-types/common/main';

type SentimentAnalysesDataBySlug = {
    [key: string]: SentimentAnalysesBySlugApiData;
};

function getSentimentAnalysesDataBySlug(): SentimentAnalysesDataBySlug {
    return {
        AMD: AMD(),
        INDO: INDO(),
        KOS: KOS(),
        NTDOF: NTDOF(),
        SHOP: SHOP(),
        TSLA: TSLA(),
    };
}

export { getSentimentAnalysesDataBySlug };

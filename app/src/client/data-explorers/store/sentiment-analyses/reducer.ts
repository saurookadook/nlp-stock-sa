import type {
    DataExplorersStore, // force formatting
    GenericReducerAction,
    GenericStateSliceReducer,
} from '@nlpssa-app-types/common/main';
import { SET_SENTIMENT_ANALYSES_BY_SLUG } from 'client/common/constants/actionTypes';
import { cleanAndTransformSentimentAnalyses } from 'client/data-explorers/utils/dataNormalizers';

type SentimentAnalysesBySlugReducer = GenericStateSliceReducer<
    DataExplorersStore['sentimentAnalysesBySlug'] | null | undefined,
    GenericReducerAction<DataExplorersStore['sentimentAnalysesBySlug']>
>;

const sentimentAnalysesBySlug: SentimentAnalysesBySlugReducer = [
    (stateSlice, action) => {
        switch (action.type) {
            case SET_SENTIMENT_ANALYSES_BY_SLUG:
                return {
                    quoteStockSymbol: action.payload?.quoteStockSymbol || '',
                    sentimentAnalyses: cleanAndTransformSentimentAnalyses(action.payload!.sentimentAnalyses),
                };
            default:
                return stateSlice;
        }
    },
    null,
];

export { sentimentAnalysesBySlug };

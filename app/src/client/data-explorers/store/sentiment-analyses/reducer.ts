import type { DataExplorersStore, GenericReducerAction, GenericStateSliceReducer } from '@nlpssa-app-types/common/main';
import { SET_SENTIMENT_ANALYSES_BY_SLUG } from 'client/common/constants/actionTypes';

type SentimentAnalysesBySlugReducer = GenericStateSliceReducer<
    DataExplorersStore['sentimentAnalysesBySlug'] | null | undefined,
    GenericReducerAction<DataExplorersStore['sentimentAnalysesBySlug']>
>;

const sentimentAnalysesBySlug: SentimentAnalysesBySlugReducer = [
    (stateSlice, action) => {
        switch (action.type) {
            case SET_SENTIMENT_ANALYSES_BY_SLUG:
                return action.payload;
            default:
                return stateSlice;
        }
    },
    null,
];

export { sentimentAnalysesBySlug };

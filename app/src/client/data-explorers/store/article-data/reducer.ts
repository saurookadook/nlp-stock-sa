import type { DataExplorersStore, GenericReducerAction, GenericStateSliceReducer } from '@nlpssa-app-types/common/main';
import { SET_ARTICLE_DATA_BY_SLUG, SET_ARTICLE_DATA } from 'client/common/constants/actionTypes';

type ArticleDataBySlugReducer = GenericStateSliceReducer<
    DataExplorersStore['articleDataBySlug'] | null | undefined,
    GenericReducerAction<DataExplorersStore['articleDataBySlug']>
>;

const articleDataBySlug: ArticleDataBySlugReducer = [
    (stateSlice, action) => {
        switch (action.type) {
            case SET_ARTICLE_DATA_BY_SLUG:
                return action.payload;
            default:
                return stateSlice;
        }
    },
    null,
];

type ArticleDataReducer = GenericStateSliceReducer<
    DataExplorersStore['articleData'] | null | undefined,
    GenericReducerAction<DataExplorersStore['articleData']>
>;

const articleData: ArticleDataReducer = [
    (stateSlice, action) => {
        switch (action.type) {
            case SET_ARTICLE_DATA:
                return action.payload;
            default:
                return stateSlice;
        }
    },
    null,
];

export { articleDataBySlug, articleData };

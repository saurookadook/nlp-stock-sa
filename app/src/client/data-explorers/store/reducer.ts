import type { DataExplorersStore, GenericReducerAction, GenericStateSliceReducer } from '@nlpssa-app-types/common/main';
import {
    SET_ARTICLE_DATA_BY_SLUG,
    SET_ARTICLE_DATA,
    SET_STOCK_DATA_ALL,
    SET_STOCK_DATA_SINGULAR,
} from 'client/common/constants/actionTypes';
import { combineReducers } from 'client/common/store/utils';

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

type StockDataAllReducer = GenericStateSliceReducer<
    DataExplorersStore['stockDataAll'] | null | undefined,
    GenericReducerAction<DataExplorersStore['stockDataAll']>
>;

const stockDataAll: StockDataAllReducer = [
    (stateSlice, action) => {
        switch (action.type) {
            case SET_STOCK_DATA_ALL:
                return action.payload;
            default:
                return stateSlice;
        }
    },
    null,
];

type StockDataSingularReducer = GenericStateSliceReducer<
    DataExplorersStore['stockDataSingular'] | null | undefined,
    GenericReducerAction<DataExplorersStore['stockDataSingular']>
>;

const stockDataSingular: StockDataSingularReducer = [
    (stateSlice, action) => {
        switch (action.type) {
            case SET_STOCK_DATA_SINGULAR:
                return action.payload;
            default:
                return stateSlice;
        }
    },
    null,
];

export default combineReducers({
    articleDataBySlug,
    articleData,
    stockDataAll,
    stockDataSingular,
});

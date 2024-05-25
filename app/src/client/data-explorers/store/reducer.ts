import type { GenericStateSliceReducer, GroupedArticleData } from '@nlpssa-app-types/common/main';
import { SET_ARTICLE_DATA } from 'client/common/constants/actionTypes';
import { combineReducers } from 'client/common/store/utils';

interface ArticleDataBySlugPageDataReducerAction {
    type: string;
    payload: GroupedArticleData;
}

const articleDataBySlug: GenericStateSliceReducer<GroupedArticleData | null, ArticleDataBySlugPageDataReducerAction> = [
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

interface ArticleDataPageDataReducerAction {
    type: string;
    payload: GroupedArticleData[];
}

const articleData: GenericStateSliceReducer<GroupedArticleData[] | null, ArticleDataPageDataReducerAction> = [
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

export default combineReducers({ articleDataBySlug, articleData });

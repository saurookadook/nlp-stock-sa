import type { GenericStateSliceReducer, GroupedArticleData } from '@nlpssa-app-types/common/main';
import { SET_ARTICLE_DATA } from 'client/common/constants/actionTypes';
import { combineReducers } from 'client/common/store/utils';

type PageData = GroupedArticleData | GroupedArticleData[];

interface PageDataReducerAction {
    type: string;
    payload: PageData;
}

// TODO: maybe this should be separated by each data entity?
const pageData: GenericStateSliceReducer<PageData | null, PageDataReducerAction> = [
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

export default combineReducers({ pageData });

import { GenericStateSliceReducer, GroupedArticleData } from '@nlpssa-app-types/common/main';
import { SET_ARTICLE_DATA } from 'client/common/constants/actionTypes';
import { user } from 'client/common/store/user/reducer';
import { combineReducers } from 'client/common/store/utils';

interface PageDataReducerAction {
    type: string;
    payload: GroupedArticleData[];
}

const pageData: GenericStateSliceReducer<GroupedArticleData[] | null, PageDataReducerAction> = [
    (stateSlice, action) => {
        switch (action.type) {
            case SET_ARTICLE_DATA:
                return [...action.payload];
            default:
                return stateSlice;
        }
    },
    null,
];

export default combineReducers({ pageData, user });

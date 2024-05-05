import { GenericStateSliceReducer } from '@nlpssa-app-types/common/main';
import { SET_ARTICLE_DATA } from 'client/common/constants/actionTypes';
import { combineReducers } from 'client/common/store/utils';

type ArticleDataEntry = {
    id: string;
    quote_stock_symbol: string;
    source_group_id: string;
    raw_content: string;
    sentence_tokens: string[];
    created_at: string;
    updated_at: string;
};

interface PageDataReducerAction {
    type: string;
    payload: ArticleDataEntry[];
}

const pageData: GenericStateSliceReducer<ArticleDataEntry[] | null, PageDataReducerAction> = [
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

export default combineReducers({ pageData });

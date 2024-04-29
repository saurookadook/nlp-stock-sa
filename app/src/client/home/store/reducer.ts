import { GenericStateSliceReducer } from '@nlpssa-app-types/common/main';
import { SET_ARTICLE_DATA } from 'client/common/constants/actionTypes';
import { combineReducers } from 'client/common/store/utils';

type ArticleDataEntry = {
    id;
    quote_stock_symbol;
    source_group_id;
    raw_content;
    sentence_tokens;
    created_at;
    updated_at;
};

interface PageDataReducerAction {
    type: string;
    payload: ArticleDataEntry[];
}

const pageData: GenericStateSliceReducer<ArticleDataEntry[], PageDataReducerAction> = [
    (stateSlice, action) => {
        switch (action.type) {
            case SET_ARTICLE_DATA:
                return [...action.payload];
            default:
                return stateSlice;
        }
    },
    [],
];

export default combineReducers({ pageData });

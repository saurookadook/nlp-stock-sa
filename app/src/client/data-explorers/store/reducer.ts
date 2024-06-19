import { combineReducers } from 'client/common/store/utils';
import * as articleDataSlices from 'client/data-explorers/store/article-data/reducer';
import * as stocksSlices from 'client/data-explorers/store/stocks/reducer';

export default combineReducers({
    ...articleDataSlices,
    ...stocksSlices,
});

import { combineReducers } from 'client/common/store/utils';
import * as userSlices from 'client/common/store/user/reducer';
import * as articleDataSlices from 'client/data-explorers/store/article-data/reducer';
import * as sentimentAnalysesSlices from 'client/data-explorers/store/sentiment-analyses/reducer';
import * as stocksSlices from 'client/data-explorers/store/stocks/reducer';

export default combineReducers({
    ...articleDataSlices,
    ...sentimentAnalysesSlices,
    ...stocksSlices,
    ...userSlices,
});

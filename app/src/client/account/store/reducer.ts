import { combineReducers } from 'client/common/store/utils';
import * as userSlices from 'client/common/store/user/reducer';

export default combineReducers({
    ...userSlices,
});

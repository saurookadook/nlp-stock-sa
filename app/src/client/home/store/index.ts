import { AppStateProviderHOC } from 'client/common/store';
import * as homeActions from './actions';
import { default as reducer } from './reducer';

const AppStateProvider = AppStateProviderHOC(reducer);

const actions = {
    ...homeActions,
};

export { AppStateProvider, actions, reducer };

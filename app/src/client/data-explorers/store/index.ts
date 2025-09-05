import { AppStateProviderHOC } from 'client/common/store';
import * as articleDataBySlugActions from './actions';
import { default as reducer } from './reducer';

const AppStateProvider = AppStateProviderHOC(reducer);

const actions = {
    ...articleDataBySlugActions,
};

export { AppStateProvider, actions, reducer };

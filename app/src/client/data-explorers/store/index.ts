import AppStateProvider from './AppStateProvider';
import * as articleDataBySlugActions from './actions';
import { default as reducer } from './reducer';

const actions = {
    ...articleDataBySlugActions,
};

export { AppStateProvider, actions, reducer };

import AppStateProvider from './AppStateProvider';
import * as homeActions from './actions';
import { default as reducer } from './reducer';

const actions = {
    ...homeActions,
};

export { AppStateProvider, actions, reducer };

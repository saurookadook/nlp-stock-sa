import { AppStateProviderHOC } from 'client/common/store';
import { default as reducer } from './reducer';

const AppStateProvider = AppStateProviderHOC(reducer);

export { AppStateProvider, reducer };

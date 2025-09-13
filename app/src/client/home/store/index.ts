import {
  AppStateProviderHOC,
  BaseStateContext,
  BaseDispatchContext,
} from 'client/common/store';
import * as homeActions from './actions';
import { default as reducer } from './reducer';

const AppStateProvider = AppStateProviderHOC({
  StateContext: BaseStateContext,
  DispatchContext: BaseDispatchContext,
  combinedReducer: reducer,
});

const actions = {
  ...homeActions,
};

export { AppStateProvider, actions, reducer };

import {
  AppStateProviderHOC,
  BaseStateContext,
  BaseDispatchContext,
} from 'client/common/store';
import * as articleDataBySlugActions from './actions';
import { default as reducer } from './reducer';

const AppStateProvider = AppStateProviderHOC({
  StateContext: BaseStateContext,
  DispatchContext: BaseDispatchContext,
  combinedReducer: reducer,
});

const actions = {
  ...articleDataBySlugActions,
};

export { AppStateProvider, actions, reducer };

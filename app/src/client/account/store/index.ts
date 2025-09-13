import {
  AppStateProviderHOC,
  BaseStateContext,
  BaseDispatchContext,
} from 'client/common/store';
import { default as reducer } from './reducer';

const AppStateProvider = AppStateProviderHOC({
  StateContext: BaseStateContext,
  DispatchContext: BaseDispatchContext,
  combinedReducer: reducer,
});

export { AppStateProvider, reducer };

import React, { useReducer } from 'react';

import { CombinedStateSliceReducer } from '@nlpssa-app-types/common/main';
import { deeplyMerge } from 'client/common/utils';

function AppStateProviderHOC<
  State = any, // force formatting
  ReducerAction = any,
  InitialState = any,
>({
  StateContext,
  DispatchContext,
  combinedReducer,
}: {
  StateContext: React.Context<State>;
  DispatchContext: React.Context<React.Dispatch<ReducerAction>>;
  combinedReducer: CombinedStateSliceReducer;
}) {
  return function AppStateProvider({
    children, // force formatting
    initialState,
  }: {
    children: React.ReactElement;
    initialState: InitialState;
  }) {
    const [combinedReducerFunc, combinedDefaultState] = combinedReducer;

    const recursivelyMergedState = deeplyMerge(combinedDefaultState, initialState);
    const [state, dispatch] = useReducer(combinedReducerFunc, recursivelyMergedState);

    return (
      <StateContext.Provider value={state}>
        <DispatchContext.Provider value={dispatch}>{children}</DispatchContext.Provider>
      </StateContext.Provider>
    );
  };
}

export default AppStateProviderHOC;

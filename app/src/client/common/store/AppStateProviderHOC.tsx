import React, { useReducer } from 'react';

import { CombinedStateSliceReducer } from '@nlpssa-app-types/common/main';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { deeplyMerge } from 'client/common/utils';

function AppStateProviderHOC<InitialState = any>(
    combinedReducer: CombinedStateSliceReducer,
) {
    return function AppStateProvider({
        children, // force formatting
        initialState,
    }: {
        children: React.ReactElement;
        initialState: InitialState;
    }) {
        const [combinedReducerFunc, combinedDefaultState] = combinedReducer;

        const recursivelyMergedState = deeplyMerge(combinedDefaultState, initialState);
        const [state, dispatch] = useReducer(
            combinedReducerFunc,
            recursivelyMergedState,
        );

        return (
            <BaseStateContext.Provider value={state}>
                <BaseDispatchContext.Provider value={dispatch}>
                    {children}
                </BaseDispatchContext.Provider>
            </BaseStateContext.Provider>
        );
    };
}

export default AppStateProviderHOC;

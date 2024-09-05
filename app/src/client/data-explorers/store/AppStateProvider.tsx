import React, { useReducer } from 'react';

import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { deeplyMerge } from 'client/common/utils';
import combinedReducer from 'client/data-explorers/store/reducer';

// TODO: fix type - React.Provider<typeof StateContext>
function AppStateProvider({
    children, // force formatting
    initialState,
}: {
    children: React.ReactElement;
    initialState?: any;
}): any {
    const [combinedReducerFunc, combinedDefaultState] = combinedReducer;

    const recursivelyMergedState = deeplyMerge(combinedDefaultState, initialState);
    const [state, dispatch] = useReducer(combinedReducerFunc, recursivelyMergedState);

    return (
        <BaseStateContext.Provider value={state}>
            <BaseDispatchContext.Provider value={dispatch}>{children}</BaseDispatchContext.Provider>
        </BaseStateContext.Provider>
    );
}

export default AppStateProvider;

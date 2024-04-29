import React, { useReducer } from 'react';

import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import combinedReducer from 'client/home/store/reducer';

// TODO: fix type - React.Provider<typeof StateContext>
function AppStateProvider({ children, initialState }: { children: React.ReactChildren; initialState: any }): any {
    const [combinedReducerFunc, combinedInitialState] = combinedReducer;

    const [state, dispatch] = useReducer(combinedReducerFunc, combinedInitialState);

    return (
        <BaseStateContext.Provider value={state}>
            <BaseDispatchContext.Provider value={dispatch}>{children}</BaseDispatchContext.Provider>
        </BaseStateContext.Provider>
    );
}

export default AppStateProvider;

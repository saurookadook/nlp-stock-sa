import {
    BaseReducerAction,
    CombinedState,
    CombinedStateSliceReducer,
    FinalReducers,
    StateSlice,
    StateSliceReducer,
} from '@nlpssa-app-types/common/main';

/**
 * @description Utility function for combining individual reducer functions and \
 * their initial state values into an Array with a single, combined reducer function \
 * and a single, combined state.
 *
 * @function combineReducers
 * @param {StateSliceReducer} reducers Map of state slices to their reducer functions
 *      (i.e. feedback: feedbackReducer, question: questionReducer)
 * @returns {CombinedStateSliceReducer} Array with a combinedReducer function and combinedState
 */
function combineReducers(reducers: StateSliceReducer): CombinedStateSliceReducer {
    const reducerKeys = Object.keys(reducers);
    const globalState: CombinedState = {};
    const finalReducers: FinalReducers = {};

    reducerKeys.forEach((key) => {
        const [reducerFunction, reducerInitialState] = reducers[key];
        if (typeof reducerFunction !== 'function') {
            throw new TypeError(`in 'combineReducers' - reducer for ${key} must be a function!`);
        } else {
            finalReducers[key] = reducerFunction;
        }
        globalState[key] = reducerInitialState;
    });
    const finalReducerKeys = Object.keys(finalReducers);

    return [
        (state: StateSlice, action: BaseReducerAction): StateSlice => {
            const newState: CombinedState = {};
            let newStateForCurrentKey = {};
            let hasStateChanged = false;

            reducerKeys.forEach((key) => {
                const currentReducer = finalReducers[key];
                const previousStateForKey = typeof state === 'object' ? state[key] : {};

                try {
                    newStateForCurrentKey = currentReducer(previousStateForKey, action);
                } catch (e) {
                    console.error(
                        `combineReducers: encountered error running reducer function for key: '${key}' and action: '${action?.type}'`,
                        e,
                    );
                    newStateForCurrentKey = previousStateForKey;
                }

                newState[key] = newStateForCurrentKey;
                hasStateChanged = hasStateChanged || newStateForCurrentKey !== previousStateForKey;
            });

            hasStateChanged = hasStateChanged || finalReducerKeys.length !== Object.keys(state).length;
            return hasStateChanged ? newState : state;
        },
        globalState,
    ];
}

export { combineReducers };

import type {
    GenericReducerAction, // force formatting
    GenericStateSliceReducer,
    UserData,
} from '@nlpssa-app-types/common/main';

type UserDataReducer = GenericStateSliceReducer<
    UserData | null | undefined, // force formatting
    GenericReducerAction<UserData>
>;

const user: UserDataReducer = [
    (stateSlice, action) => {
        switch (action.type) {
            default:
                return stateSlice;
        }
    },
    null,
];

export { user };

import type {
    GenericReducerAction, // force formatting
    GenericStateSliceReducer,
    UserData,
} from '@nlpssa-app-types/common/main';
import { COMPLETE_LOGOUT } from 'client/common/constants/actionTypes';

type UserDataReducer = GenericStateSliceReducer<
    UserData | null | undefined, // force formatting
    GenericReducerAction<UserData>
>;

const user: UserDataReducer = [
    (stateSlice, action) => {
        switch (action.type) {
            case COMPLETE_LOGOUT:
                return null;
            default:
                return stateSlice;
        }
    },
    null,
];

export { user };

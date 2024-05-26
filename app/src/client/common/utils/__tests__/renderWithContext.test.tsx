/* eslint-disable react/prop-types */
import * as React from 'react';
import { cleanup, screen, waitFor } from '@testing-library/react';

import { BaseReducerAction } from '@nlpssa-app-types/common/main';
import { deeplyMerge } from 'client/common/utils';
import renderWithContext from 'client/common/utils/renderWithContext';
import { combineReducers } from 'client/common/store/utils';

const mockActions = {
    INCREMENT_COUNT: 'INCREMENT_COUNT',
    INIT_PAGE: 'INIT_PAGE',
};

type MockStateStore = {
    locals: { count: number };
    pageData: PageDataStateSlice;
    user: UserStateSlice;
};

const MockStateContext = React.createContext<MockStateStore>({
    locals: { count: 0 },
    pageData: {},
    user: {},
});
const MockDispatchContext = React.createContext<React.Dispatch<BaseReducerAction>>((action) => action);

const mockLocalsStateSlice = [
    (stateSlice, action) => {
        switch (action.type) {
            case mockActions.INCREMENT_COUNT:
                stateSlice.count += 1;
                return stateSlice;
            default:
                return stateSlice;
        }
    },
    {
        count: 0,
    },
];

const mockPageDataStateSlice = [
    (stateSlice, action) => {
        switch (action.type) {
            case mockActions.INIT_PAGE:
                return {
                    ...stateSlice,
                    ...action.payload.pageData,
                };
            default:
                return stateSlice;
        }
    },
    null,
];

const mockUserStateSlice = [
    (stateSlice, action) => {
        switch (action.type) {
            case mockActions.INIT_PAGE:
                return {
                    ...stateSlice,
                    ...action.payload.user,
                };
            default:
                return stateSlice;
        }
    },
    null,
];

const [mockCombinedReducer, mockCombinedDefaultState] = combineReducers({
    locals: mockLocalsStateSlice,
    pageData: mockPageDataStateSlice,
    user: mockUserStateSlice,
});

type PageDataStateSlice = {
    certainty?: number;
    data?: string[];
    sentiment?: string;
    stockSlug?: string;
};

const initialPageDataStateSlice: PageDataStateSlice = {
    certainty: 0.99,
    data: ['stuff', 'moar stuff', 'furrballz'],
    sentiment: 'SUPER GREAT',
    stockSlug: 'MEOW',
};

type UserStateSlice = {
    firstName?: string;
    lastName?: string;
    isBlocked?: boolean;
};

const initialUserStateSlice: UserStateSlice = {
    firstName: 'Testy',
    lastName: 'McTestermanjensensonmann',
    isBlocked: false,
};

const initPageAction = ({ dispatch, data }) =>
    dispatch({
        type: mockActions.INIT_PAGE,
        data,
    });

const incrementCountAction = ({ dispatch }) => dispatch({ type: mockActions.INCREMENT_COUNT });

const MockProvider = ({ children, initialState }) => {
    const recursivelyMergedState = deeplyMerge(mockCombinedDefaultState, initialState);
    const [state, dispatch] = React.useReducer(mockCombinedReducer, recursivelyMergedState);

    return (
        <MockStateContext.Provider value={state}>
            <MockDispatchContext.Provider value={dispatch}>{children}</MockDispatchContext.Provider>
        </MockStateContext.Provider>
    );
};

const renderStateSlices = (state: MockStateStore) => {
    const stateSliceKeys = Object.keys(state);
    return stateSliceKeys.map((sliceKey, i) => {
        const stateSlice = state[sliceKey];
        const stateSliceProperties = Object.keys(stateSlice);
        return (
            <ul key={`${sliceKey}-${i}`} id={`${sliceKey}`}>
                {stateSliceProperties.map((property, j) => {
                    return <li key={`${property}-${j}`}>{`${property}: ${stateSlice[property]}`}</li>;
                })}
            </ul>
        );
    });
};

const MockComponentUnderTest = () => {
    const { locals, pageData, user } = React.useContext(MockStateContext);
    const dispatch = React.useContext(MockDispatchContext);

    const hasInitialized = () => pageData != null && user != null;

    React.useEffect(() => {
        if (!hasInitialized()) {
            setTimeout(() => {
                return initPageAction({
                    dispatch,
                    data: {
                        pageData: initialPageDataStateSlice,
                        user: initialUserStateSlice,
                    },
                });
            });
        }
    }, [locals.count, pageData, user]);

    return (
        <div id="main-container">
            <section>
                <span id="count">{`Current count: ${locals.count}`}</span>
                <button onClick={() => incrementCountAction({ dispatch })}>{`PRESS THE BUTTON`}</button>
            </section>
            <div className="state-slices-wrapper">
                {hasInitialized() ? (
                    <span aria-label="state slices">{renderStateSlices({ locals, pageData, user })}</span>
                ) : (
                    <span aria-label="Loading...">{`Loading... 🙃`}</span>
                )}
            </div>
        </div>
    );
};

describe('renderWithContext utility', () => {
    beforeEach(() => {
        cleanup();
    });

    afterAll(() => {
        cleanup();
    });

    it('should render the component under test', async () => {
        renderWithContext(<MockComponentUnderTest />, MockProvider);

        expect(screen.getAllByLabelText('Loading...')).toBeVisible();

        await waitFor(() => {
            const stateSlicesElement = screen.getByLabelText('state slices');
            expect(stateSlicesElement).toBeVisible();
            expect(stateSlicesElement.querySelectorAll('#pageData > li')).toHaveLength(4);
            expect(stateSlicesElement.querySelectorAll('#user > li')).toHaveLength(3);
        });
    });

    it("should render the component correctly based on the passed 'state'", async () => {
        renderWithContext(<MockComponentUnderTest />, MockProvider, {
            state: {
                pageData: {
                    certainty: 0.97,
                    sentiment: 'haz gud snoot',
                    stockSlug: 'WOOF',
                },
                user: {
                    firstName: 'Hooplah',
                    isBlocked: false,
                },
            },
        });

        await waitFor(() => {
            const stateSlicesElement = screen.getByLabelText('state slices');
            expect(stateSlicesElement).toBeVisible();
            expect(stateSlicesElement.querySelectorAll('#pageData > li')).toHaveLength(3);
            expect(stateSlicesElement.querySelectorAll('#user > li')).toHaveLength(2);
        });
    });

    it('should handle user interaction correctly in the component under test', async () => {
        const { user } = renderWithContext(<MockComponentUnderTest />, MockProvider);

        const getCountElement = () => screen.getByText(/Current\scount:\s\d+/);

        expect(getCountElement()).toHaveTextContent('Current count: 0');

        await user.click(screen.getByRole('button'));

        await waitFor(() => {
            expect(getCountElement()).toHaveTextContent('Current count: 1');
        });
    });
});

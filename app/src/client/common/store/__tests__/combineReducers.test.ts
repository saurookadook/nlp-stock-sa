import { combineReducers } from 'client/common/store/utils';

const mockActions = {
    ADD_FLASH_MESSAGE: 'ADD_FLASH_MESSAGE',
    INIT_PAGE: 'INIT_PAGE',
    SET_IT_ON_FIRE: 'SET_IT_ON_FIRE',
    UPDATE_USER_IS_BLOCKED: 'UPDATE_USER_IS_BLOCKED',
};

type LocalsStateSlice = {
    flashMessages?: string[];
    pathname?: string;
};

const defaultLocalsStateSlice: LocalsStateSlice = {
    pathname: '/app/home',
};

const mockLocalsReducer = [
    (stateSlice: LocalsStateSlice = {}, action) => {
        switch (action.type) {
            case mockActions.ADD_FLASH_MESSAGE:
                if (!Array.isArray(stateSlice.flashMessages)) stateSlice.flashMessages = [];
                stateSlice.flashMessages.push(action.payload.flashMessage);
                return stateSlice;
            case mockActions.INIT_PAGE:
                return {
                    ...stateSlice,
                    ...action.payload.locals,
                };
            default:
                return stateSlice;
        }
    },
    defaultLocalsStateSlice,
];

type UserStateSlice = {
    firstName?: string;
    lastName?: string;
    isBlocked?: boolean;
};

const defaultUserStateSlice: UserStateSlice = {
    firstName: 'Testy',
    lastName: 'McTestermanjensensonmann',
    isBlocked: false,
};

const mockUserReducer = [
    (stateSlice: UserStateSlice = {}, action) => {
        switch (action.type) {
            case mockActions.UPDATE_USER_IS_BLOCKED:
                stateSlice.isBlocked = action.payload.isBlocked;
                return stateSlice;
            case mockActions.INIT_PAGE:
                return action.payload.user != null
                    ? {
                          ...stateSlice,
                          ...action.payload.user,
                      }
                    : stateSlice;
            default:
                return stateSlice;
        }
    },
    defaultUserStateSlice,
];

describe('combineReducers utility', () => {
    let testCombinedReducer, testCombinedInitialState;
    // to make test output quieter :]
    jest.spyOn(console, 'error').mockImplementation((...args) => args);

    beforeEach(() => {
        [testCombinedReducer, testCombinedInitialState] = combineReducers({
            locals: mockLocalsReducer,
            user: mockUserReducer,
        });
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    afterAll(() => {
        jest.restoreAllMocks();
    });

    it('combines default states', () => {
        const expectedDefaultState = {
            locals: defaultLocalsStateSlice,
            user: defaultUserStateSlice,
        };
        expect(testCombinedInitialState).toEqual(expectedDefaultState);
    });

    describe('returned combined reducer', () => {
        it("does not change state on 'null' action payload", () => {
            const sameAsDefaultState = testCombinedReducer(testCombinedInitialState, { type: 'LOLZ' });
            expect(testCombinedInitialState).toEqual(sameAsDefaultState);
        });

        describe('applies state change only to slice of state for corresponding action', () => {
            it("only applies change to 'locals' state slice", () => {
                const mockFlashMessage = 'LOOK OUT BEHIND YOU! 😱';
                const stateWithFlashMessage = testCombinedReducer(testCombinedInitialState, {
                    type: mockActions.ADD_FLASH_MESSAGE,
                    payload: { flashMessage: mockFlashMessage },
                });
                const expectedUpdatedState = {
                    locals: {
                        ...defaultLocalsStateSlice,
                        flashMessages: [mockFlashMessage],
                    },
                    user: {
                        ...defaultUserStateSlice,
                    },
                };
                expect(stateWithFlashMessage).toEqual(expectedUpdatedState);
            });

            it("only applies change to 'user' state slice", () => {
                const stateUserIsBlocked = testCombinedReducer(testCombinedInitialState, {
                    type: mockActions.UPDATE_USER_IS_BLOCKED,
                    payload: { isBlocked: true },
                });
                const expectedUpdatedState = {
                    locals: {
                        ...defaultLocalsStateSlice,
                    },
                    user: {
                        ...defaultUserStateSlice,
                        isBlocked: true,
                    },
                };
                expect(stateUserIsBlocked).toEqual(expectedUpdatedState);
            });

            it('changes more than one slice of state based on action', () => {
                const mockLocalsSlice = {
                    flashMessages: ["Sorry, Santa; those cookies weren't for you but we saw you eat them anyway..."],
                    pathname: '/app/blocked',
                };
                const mockUserSlice = {
                    firstName: 'Santa',
                    lastName: 'Claus',
                    isBlocked: true,
                };

                const stateAfterInitPage = testCombinedReducer(testCombinedInitialState, {
                    type: mockActions.INIT_PAGE,
                    payload: {
                        locals: {
                            ...mockLocalsSlice,
                        },
                        user: {
                            ...mockUserSlice,
                        },
                    },
                });
                const expectedUpdatedState = {
                    locals: mockLocalsSlice,
                    user: mockUserSlice,
                };

                expect(stateAfterInitPage).toEqual(expectedUpdatedState);
            });
        });

        describe('handles problems as expected', () => {
            it('raises error for non-function reducers', () => {
                expect(() => {
                    const [combinedWoopsReducer, combinedWoopsState] = combineReducers({
                        woops: ['enchantment?', { excitedGreeting: 'enchantment!' }],
                    });
                }).toThrow();
            });

            it('logs error and returns existing state slice if error is encountered in reducer', () => {
                const mockProblematicReducer = (stateSlice = {}, action) => {
                    switch (action.type) {
                        case mockActions.SET_IT_ON_FIRE:
                            return JSON.parse('{"lolz": "woooooooppppppppsssiiiiieeeeeeeeeeez",');
                        default:
                            return stateSlice;
                    }
                };

                const [combinedWoopsReducer, combinedWoopsState] = combineReducers({
                    woops: [mockProblematicReducer, { excitedGreeting: 'enchantment!', query: 'enchantment?' }],
                });
                const expectedWoopsState = {
                    woops: { excitedGreeting: 'enchantment!', query: 'enchantment?' },
                };

                expect(combinedWoopsState).toEqual(expectedWoopsState);

                const uhOhBrokenWoopsState = combinedWoopsReducer(combinedWoopsState, {
                    type: mockActions.SET_IT_ON_FIRE,
                    payload: { worriedGreeting: 'enchantment...?' },
                });

                expect(uhOhBrokenWoopsState).toEqual(combinedWoopsState);
            });
        });
    });
});

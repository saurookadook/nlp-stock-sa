import { Dispatch, createContext } from 'react';

import { StateSlice, BaseReducerAction } from '@nlpssa-app-types/common/main';

export const BaseStateContext = createContext<StateSlice>({});
export const BaseDispatchContext = createContext<Dispatch<BaseReducerAction>>((action) => action);

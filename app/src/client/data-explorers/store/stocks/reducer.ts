import type { DataExplorersStore, GenericReducerAction, GenericStateSliceReducer } from '@nlpssa-app-types/common/main';
import { SET_STOCK_DATA_ALL, SET_STOCK_DATA_SINGULAR } from 'client/common/constants/actionTypes';

type StockDataAllReducer = GenericStateSliceReducer<
    DataExplorersStore['stockDataAll'] | null | undefined,
    GenericReducerAction<DataExplorersStore['stockDataAll']>
>;

const stockDataAll: StockDataAllReducer = [
    (stateSlice, action) => {
        switch (action.type) {
            case SET_STOCK_DATA_ALL:
                return action.payload;
            default:
                return stateSlice;
        }
    },
    null,
];

type StockDataSingularReducer = GenericStateSliceReducer<
    DataExplorersStore['stockDataSingular'] | null | undefined,
    GenericReducerAction<DataExplorersStore['stockDataSingular']>
>;

const stockDataSingular: StockDataSingularReducer = [
    (stateSlice, action) => {
        switch (action.type) {
            case SET_STOCK_DATA_SINGULAR:
                return action.payload;
            default:
                return stateSlice;
        }
    },
    null,
];

export { stockDataAll, stockDataSingular };

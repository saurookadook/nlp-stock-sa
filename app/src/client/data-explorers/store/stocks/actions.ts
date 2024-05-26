import { SET_STOCK_DATA_ALL, SET_STOCK_DATA_SINGULAR } from 'client/common/constants/actionTypes';

export const fetchSingularStockData = async ({ dispatch, stockSlug }) => {
    try {
        const apiResponse = await fetch(`/api/stocks/${stockSlug}`);

        if (apiResponse.status >= 400) {
            const errorResponse = await apiResponse.text();
            throw new Error(errorResponse);
        }

        const apiData = await apiResponse.json();

        if (apiData.detail) {
            throw new Error(apiData.detail);
        }

        console.log('fetchSingularStockData - apiData: ', { apiData });
        return setStockDataSingular({ dispatch, stockDataSingular: apiData.data });
    } catch (e) {
        console.warn('[data-explorers.stocks : fetchSingularStockData] - caught exception', e);
    }
};

export const fetchAllStockData = async ({ dispatch }) => {
    try {
        const apiResponse = await fetch(`/api/stocks`);

        if (apiResponse.status >= 400) {
            const errorResponse = await apiResponse.text();
            throw new Error(errorResponse);
        }

        const apiData = await apiResponse.json();

        if (apiData.detail) {
            throw new Error(apiData.detail);
        }

        console.log('fetchAllStockData - apiData: ', { apiData });
        return setStockDataAll({ dispatch, stockDataAll: apiData.data });
    } catch (e) {
        console.warn('[data-explorers.stocks : fetchAllStockData] - caught exception', e);
    }
};

export const setStockDataSingular = ({ dispatch, stockDataSingular }): void => {
    return dispatch({ type: SET_STOCK_DATA_SINGULAR, payload: stockDataSingular });
};

export const setStockDataAll = ({ dispatch, stockDataAll }): void => {
    return dispatch({ type: SET_STOCK_DATA_ALL, payload: stockDataAll });
};

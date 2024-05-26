import { SET_ARTICLE_DATA_BY_SLUG, SET_ARTICLE_DATA } from 'client/common/constants/actionTypes';

export const fetchArticleDataByStockSlug = async ({ dispatch, stockSlug }) => {
    try {
        const apiResponse = await fetch(`/api/article-data/${stockSlug}`);

        if (apiResponse.status >= 400) {
            const errorResponse = await apiResponse.text();
            throw new Error(errorResponse);
        }

        const apiData = await apiResponse.json();

        if (apiData.detail) {
            throw new Error(apiData.detail);
        }

        console.log('fetchArticleDataByStockSlug - apiData: ', { apiData });
        return setArticleDataBySlug({ dispatch, articleDataBySlug: apiData.data });
    } catch (e) {
        console.warn('[data-explorers.article-data : fetchArticleDataByStockSlug] - caught exception', e);
    }
};

export const fetchAllArticleData = async ({ dispatch }) => {
    try {
        const apiResponse = await fetch(`/api/article-data`);

        if (apiResponse.status >= 400) {
            const errorResponse = await apiResponse.text();
            throw new Error(errorResponse);
        }

        const apiData = await apiResponse.json();

        if (apiData.detail) {
            throw new Error(apiData.detail);
        }

        console.log('fetchAllArticleData - apiData: ', { apiData });
        return setArticleData({ dispatch, articleData: apiData.data });
    } catch (e) {
        console.warn('[data-explorers.article-data : fetchAllArticleData] - caught exception', e);
    }
};

export const setArticleDataBySlug = ({ dispatch, articleDataBySlug }): void => {
    return dispatch({ type: SET_ARTICLE_DATA_BY_SLUG, payload: articleDataBySlug });
};

export const setArticleData = ({ dispatch, articleData }): void => {
    return dispatch({ type: SET_ARTICLE_DATA, payload: articleData });
};

import { SET_ARTICLE_DATA } from 'client/common/constants/actionTypes';

export const fetchArticleDataByStockSlug = async ({ dispatch, stockSlug }) => {
    try {
        // http://localhost:3000/api/article-data
        const apiResponse = await fetch(`/api/article-data/${stockSlug}`);
        const apiData = await apiResponse.json();

        if (apiData.detail) {
            throw new Error(apiData.detail);
        }

        console.log('fetchArticleDataByStockSlug - apiData: ', { apiData });
        return setArticleData({ dispatch, articleData: apiData.data });
    } catch (e) {
        console.warn('[home fetchArticleDataByStockSlug] - caught exception', e);
    }
};

export const setArticleData = ({ dispatch, articleData }): void => {
    return dispatch({ type: SET_ARTICLE_DATA, payload: articleData });
};

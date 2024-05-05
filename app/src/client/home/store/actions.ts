import { SET_ARTICLE_DATA } from 'client/common/constants/actionTypes';

export const fetchArticleData = async ({ dispatch }) => {
    try {
        // http://localhost:3000/api/article-data
        const apiResponse = await fetch('/api/article-data');
        const apiData = await apiResponse.json();

        if (apiData.detail) {
            throw new Error(apiData.detail);
        }

        console.log('fetchArticleData - apiData: ', { apiData });
        return setArticleData({ dispatch, articleData: apiData.data });
    } catch (e) {
        console.warn('[home fetchArticleData] - caught exception', e);
    }
};

export const setArticleData = ({ dispatch, articleData }): void => {
    return dispatch({ type: SET_ARTICLE_DATA, payload: articleData });
};

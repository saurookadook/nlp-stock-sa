import { SET_SENTIMENT_ANALYSES_BY_SLUG } from 'client/common/constants/actionTypes';

export const fetchSentimentAnalysesByStockSlug = async ({ dispatch, stockSlug }) => {
    try {
        const apiResponse = await fetch(`/api/sentiment-analyses/${stockSlug}`);

        if (apiResponse.status >= 400) {
            const errorResponse = await apiResponse.text();
            throw new Error(errorResponse);
        }

        const apiData = await apiResponse.json();

        if (apiData.detail) {
            throw new Error(apiData.detail);
        }

        console.log('fetchSentimentAnalysesByStockSlug - apiData: ', { apiData });
        return setSentimentAnalysesBySlug({ dispatch, sentimentAnalysesBySlug: apiData.data });
    } catch (e) {
        console.warn('[data-explorers.sentiment-analyses : fetchSentimentAnalysesByStockSlug] - caught exception', e);
    }
};

export const setSentimentAnalysesBySlug = ({ dispatch, sentimentAnalysesBySlug }): void => {
    return dispatch({ type: SET_SENTIMENT_ANALYSES_BY_SLUG, payload: sentimentAnalysesBySlug });
};

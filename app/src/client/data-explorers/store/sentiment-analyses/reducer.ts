import type {
    DataExplorersStore,
    GenericReducerAction,
    GenericStateSliceReducer,
    SentimentAnalysesDataEntry,
} from '@nlpssa-app-types/common/main';
import { SET_SENTIMENT_ANALYSES_BY_SLUG } from 'client/common/constants/actionTypes';
import { safeGetDateValue } from 'client/common/components/MultiSeriesLineGraph/utils';

type SentimentAnalysesBySlugReducer = GenericStateSliceReducer<
    DataExplorersStore['sentimentAnalysesBySlug'] | null | undefined,
    GenericReducerAction<DataExplorersStore['sentimentAnalysesBySlug']>
>;

function compareByDateCallback(a: SentimentAnalysesDataEntry, b: SentimentAnalysesDataEntry) {
    const aField = safeGetDateValue(a);
    const bField = safeGetDateValue(b);

    return aField == bField ? 0 : Number(aField > bField) - Number(aField < bField);
}

function dateFieldIsValid(dateField: unknown) {
    return dateField != null && typeof dateField === 'string' && dateField !== '';
}

function cleanAndTransformSentimentAnalyses(data: SentimentAnalysesDataEntry[] | undefined) {
    return data != null && data.length < 1
        ? []
        : (data as SentimentAnalysesDataEntry[])
              .filter((d) => d.source != null)
              .map(function (d) {
                  if (dateFieldIsValid(d.source?.data?.last_updated_date)) {
                      d.source!.data!.last_updated_date = new Date(d.source!.data!.last_updated_date as string);
                  }
                  if (dateFieldIsValid(d.source?.data?.published_date)) {
                      d.source!.data!.published_date = new Date(d.source!.data!.published_date as string);
                  }
                  if (dateFieldIsValid(d.source?.updated_at)) {
                      d.source!.updated_at = new Date(d.source!.updated_at);
                  }
                  return d;
              })
              .sort(compareByDateCallback);
}

const sentimentAnalysesBySlug: SentimentAnalysesBySlugReducer = [
    (stateSlice, action) => {
        switch (action.type) {
            case SET_SENTIMENT_ANALYSES_BY_SLUG:
                return {
                    quoteStockSymbol: action.payload?.quoteStockSymbol || '',
                    sentimentAnalyses: cleanAndTransformSentimentAnalyses(action.payload!.sentimentAnalyses),
                };
            default:
                return stateSlice;
        }
    },
    null,
];

export { sentimentAnalysesBySlug };

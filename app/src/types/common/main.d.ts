import 'react';

type AmbiguousObject = Record<string, unknown>;

declare module '*.svg' {
    const content: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
    export default content;
}

declare global {
    type RenderAppFunc = (data: AmbiguousObject) => void;

    var renderApp: RenderAppFunc;
    var $fetchArticle: ({ dispatch }: { dispatch: any }) => Promise<void>;
    // interface Window {
    //     renderApp: RenderAppFunc;
    // }
}

/**********************************************************************
 * Generic State Store Types
 **********************************************************************/
type StateSlice = {
    [key: string]: AmbiguousObject | AmbiguousObject[];
};

interface CombinedState extends StateSlice {
    pageData?: StateSlice;
}

interface BaseReducerAction {
    type: string;
    payload?: StateSlice;
}

type GenericReducerFunc<S, A> = (state: S, action: A) => S;

type StateSliceReducerFunc = (state: StateSlice, action: BaseReducerAction) => StateSlice;

type GenericStateSliceReducer<S, A> = [GenericReducerFunc<S, A>, S];

interface StateSliceReducer {
    [key: string]: GenericStateSliceReducer;
}

type CombinedStateSliceReducer = [GenericReducerFunc, CombinedState];

interface FinalReducers {
    [key: string]: GenericReducerFunc;
}

/**********************************************************************
 * Article Data
 **********************************************************************/
type ArticleDataEntry = {
    id: string;
    quoteStockSymbol: string;
    sourceGroupId: string;
    sourceUrl: string;
    createdAt: string;
    updatedAt: string;
    author?: string;
    lastUpdatedDate?: string;
    publishedDate?: string;
    rawContent?: string;
    sentenceTokens?: string;
    thumbnailImageUrl?: string;
    title?: string;
};

type GroupedArticleData = {
    quoteStockSymbol: string;
    articleData: ArticleDataEntry[];
};

type AbstractPageData = {
    data: GroupedArticleData | GroupedArticleData[] | null;
};

type ArticleDataBySlugViewStore = {
    articleDataBySlug: GroupedArticleData;
};

type ArticleDataViewStore = {
    articleData: GroupedArticleData[];
};

type InitialArticleDataBySlugPageData = {
    data: GroupedArticleData | null;
};

type InitialHomePageData = {
    data: GroupedArticleData[] | null;
};

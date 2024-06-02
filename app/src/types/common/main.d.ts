import 'react';

type AmbiguousObject = Record<string, unknown>;

type NullableValue<V> = V | null;

type NullableObject<T> = {
    [K in keyof T]: NullableValue<T[K]>;
};

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
type GenericStateStore<V> = {
    [K in keyof V]: V[K] | null;
};

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

type GenericReducerAction<T> = {
    type: string;
    payload?: T;
};

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

type ArticleDataBySlugApiData = {
    data: GroupedArticleData | null;
};

type InitialArticleDataBySlugExplorerPageData = ArticleDataBySlugApiData;

type ArticleDataApiData = {
    data: GroupedArticleData[] | null;
};

type InitialArticleDataExplorerPageData = ArticleDataApiData;

type InitialHomePageData = {
    data: GroupedArticleData[] | null;
};

type AbstractPageData = {
    data: GroupedArticleData | GroupedArticleData[] | null;
};

/**********************************************************************
 * Stocks
 **********************************************************************/
type StockDataEntry = {
    id: string;
    quoteStockSymbol: string;
    fullStockSymbol: string;
    exchangeName?: string;
    createdAt: string;
    updatedAt: string;
};

type AllStockData = {
    data: StockDataEntry[] | null;
};

type SingularStockData = {
    data: StockDataEntry | null;
};

/**********************************************************************
 * Data Explorers
 **********************************************************************/
type ArticleDataBySlugStateSlice = GroupedArticleData;
type ArticleDataStateSlice = GroupedArticleData[];
type StockDataAllStateSlice = StockDataEntry[];
type StockDataSingularStateSlice = StockDataEntry;

type DataExplorersStore = {
    articleDataBySlug: ArticleDataBySlugStateSlice;
    articleData: ArticleDataStateSlice;
    stockDataAll: StockDataAllStateSlice;
    stockDataSingular: StockDataSingularStateSlice;
};

/**********************************************************************
 * Home
 **********************************************************************/
type HomeStore = {
    pageData: GroupedArticleData[] | null;
};

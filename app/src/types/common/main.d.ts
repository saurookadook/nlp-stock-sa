import 'react';
import React from 'react';

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
    type RenderAppFunc = (data: AmbiguousObject) => Promise<void>;

    var renderApp: RenderAppFunc;
    // var $fetchArticle: ({ dispatch }: { dispatch: any }) => Promise<void>;
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
 * Users
 **********************************************************************/
type UserData = {
    firstName?: string;
    lastName?: string;
    username: string;
};

/**********************************************************************
 * Home
 **********************************************************************/
type HomeStore = {
    pageData: NullableValue<GroupedArticleData[]>;
    user: NullableValue<UserData>;
};

/**********************************************************************
 * Source
 **********************************************************************/
type SourceDiscriminator = 'article_data' | 'reddit_data';

type Source = {
    id: string;
    data_type_id: NullableValue<string>;
    data_type: NullableValue<SourceDiscriminator>;
    data: NullableValue<ArticleDataEntry>;
};

/**********************************************************************
 * Article Data
 **********************************************************************/
type ArticleDataEntry = {
    id: string;
    quoteStockSymbol: string;
    sourceGroupId: string;
    sourceUrl: string;
    source: NullableValue<Source>;
    createdAt: string | Date;
    updatedAt: string | Date;
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
 * Sentiment Analyses
 **********************************************************************/
type SASourceData = {
    created_at: string | Date;
    updated_at: string | Date;
    id: string;
    quote_stock_symbol: string;
    source_group_id: string;
    source_url: string;
    polymorphic_source: null;
    author: string;
    last_updated_date?: string | Date;
    published_date?: string | Date;
    raw_content: string;
    sentence_tokens: string;
    thumbnail_image_url: string;
    title: string;
};

type SASource = {
    // TODO: temp until I can get nested models to have their properties transformed correctly
    created_at: string | Date;
    updated_at: string | Date;
    id: string;
    data_type_id: string;
    data_type: string;
    data: NullableValue<SASourceData>;
    source_owner_name: string;
};

type SentimentAnalysisOutput = {
    compound: number;
    neg: number;
    neu: number;
    pos: number;
};

type SentimentEnum = 'compound' | 'negative' | 'neutral' | 'positive';

type SentimentAnalysesDataEntry = {
    id: string;
    quoteStockSymbol: string;
    sourceGroupId?: string;
    sourceId: NullableValue<string>;
    source: NullableValue<SASource>; // TODO: make it better
    output: SentimentAnalysisOutput;
    score: number;
    sentiment: SentimentEnum;
    createdAt: string | Date;
    updatedAt: string | Date;
};

type SentimentAnalysesBySlugApiData = {
    quoteStockSymbol: string;
    sentimentAnalyses: SentimentAnalysesDataEntry[];
};

type SentimentAnalysesBySlugApiResponse = {
    data: SentimentAnalysesBySlugApiData | null;
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
type SentimentAnalysesBySlugStateSlice = SentimentAnalysesBySlugApiData;
type StockDataAllStateSlice = StockDataEntry[];
type StockDataSingularStateSlice = StockDataEntry;

type DataExplorersStore = {
    articleDataBySlug: ArticleDataBySlugStateSlice;
    articleData: ArticleDataStateSlice;
    sentimentAnalysesBySlug: SentimentAnalysesBySlugStateSlice;
    stockDataAll: StockDataAllStateSlice;
    stockDataSingular: StockDataSingularStateSlice;
};

/**********************************************************************
 * Graph
 **********************************************************************/
type GraphConfig<DataType> = {
    initialWidth: number;
    data: DataType[];
    legend: {
        itemSize: number;
        spacer: number;
    };
    height: number;
    margins: {
        top: number;
        right: number;
        bottom: number;
        left: number;
    };
    width: number;
    xScale: AxisScaleFnX;
    yScale: AxisScaleFnY;
};

type MSLGraphContext = {
    graphConfig: GraphConfig;
    setGraphConfig: SetStateFunc<GraphConfig>;
};

type MSLGraphConfig = GraphConfig<SentimentAnalysesDataEntry>;

/**********************************************************************
 * D3 (custom)
 **********************************************************************/
type AxisTuple = [number, number, never];
type AxisScaleFnX = d3.ScaleTime<AxisTuple>;
type AxisScaleFnY = d3.ScaleLinear<AxisTuple>;
type D3Point = [number, number, string];
type DispatchParams = d3.CustomEventParameters & { bubble?: boolean };

/**********************************************************************
 * React (custom)
 **********************************************************************/
type SetStateFunc<T> = React.Dispatch<React.SetStateAction<T>>;

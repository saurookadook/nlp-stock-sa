import React from 'react';
import { createBrowserRouter } from 'react-router-dom';

import { ErrorElement } from 'client/common/layouts';
import ArticleDataBySlugExplorer from 'client/data-explorers/explorers/article-data/ArticleDataBySlugExplorer';
import ArticleDataExplorer from 'client/data-explorers/explorers/article-data/ArticleDataExplorer';
import SentimentAnalysesBySlugExplorer from 'client/data-explorers/explorers/sentiment-analyses/SentimentAnalysesBySlugExplorer';
import AllStocksExplorer from 'client/data-explorers/explorers/stocks/AllStocksExplorer';
import SingleStockExplorer from 'client/data-explorers/explorers/stocks/SingleStockExplorer';
import DataExplorerView from 'client/data-explorers/layouts/DataExplorerView';
import ExplorersList from 'client/data-explorers/explorers/list/ExplorersList';

export const dataExplorersRoutes = [
    {
        path: '/data-explorers',
        element: <DataExplorerView />,
        errorElement: <ErrorElement />,
        children: [
            {
                path: 'article-data/:stockSlug',
                element: <ArticleDataBySlugExplorer />,
            },
            {
                path: 'article-data',
                element: <ArticleDataExplorer />,
            },
            {
                path: 'sentiment-analyses/:stockSlug',
                element: <SentimentAnalysesBySlugExplorer />,
            },
            {
                path: 'stocks/:stockSlug',
                element: <SingleStockExplorer />,
            },
            {
                path: 'stocks',
                element: <AllStocksExplorer />,
            },
            {
                path: '',
                element: <ExplorersList />,
            },
        ],
    },
];

export default createBrowserRouter(dataExplorersRoutes, { basename: '/app' });

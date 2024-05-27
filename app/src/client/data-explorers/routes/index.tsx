import React from 'react';
import { createBrowserRouter } from 'react-router-dom';

import { ErrorElement } from 'client/common/layouts';
import {
    ArticleDataBySlugExplorer,
    ArticleDataExplorer,
    AllStocksExplorer,
    SingleStockExplorer,
} from 'client/data-explorers/explorers';
import { DataExplorerView } from 'client/data-explorers/layouts';

export default createBrowserRouter([
    {
        path: '/app/data-explorers',
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
                path: 'stocks/:stockSlug',
                element: <SingleStockExplorer />,
            },
            {
                path: 'stocks',
                element: <AllStocksExplorer />,
            },
        ],
    },
]);

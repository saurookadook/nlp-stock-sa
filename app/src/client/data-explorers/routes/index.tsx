import React from 'react';

import { ErrorElement } from 'client/common/layouts';
import {
    ArticleDataBySlugExplorer,
    ArticleDataExplorer,
    AllStocksExplorer,
    SingleStockExplorer,
} from 'client/data-explorers/explorers';
import { DataExplorerView } from 'client/data-explorers/layouts';

export const dataExplorersRoutes = [
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
];

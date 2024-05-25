import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import type { AbstractPageData } from '@nlpssa-app-types/common/main';
import { BasePage, ErrorElement } from 'client/common/layouts';
import { ArticleDataBySlugView, ArticleDataView } from 'client/data-explorers/article-data/components';
import { DataExplorerView } from 'client/data-explorers/layouts';
import AppStateProvider from 'client/data-explorers/store/AppStateProvider';

function BaseDataExplorer({ initialPageData }: { initialPageData: AbstractPageData }) {
    const browserRouter = createBrowserRouter([
        {
            path: '/data-explorers',
            element: <DataExplorerView />,
            errorElement: <ErrorElement />,
            children: [
                {
                    path: 'article-data/:stockSlug',
                    element: <ArticleDataBySlugView />,
                },
                {
                    path: 'article-data',
                    element: <ArticleDataView />,
                },
                // {
                //     path: 'stocks/:stockSlug',
                //     element: <ArticleDataBySlugView />,
                // },
                // {
                //     path: 'stocks',
                //     element: <ArticleDataView />,
                // },
            ],
        },
    ]);

    console.log('data-explorers - BaseDataExplorer', { initialPageData });
    return (
        <BasePage>
            <AppStateProvider initialState={initialPageData}>
                <RouterProvider router={browserRouter} />
            </AppStateProvider>
        </BasePage>
    );
}

export default BaseDataExplorer;

import React, { useContext } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import type { InitialArticleDataBySlugPageData } from '@nlpssa-app-types/common/main';
import { BasePage, ErrorElement } from 'client/common/layouts';
import { BaseStateContext } from 'client/common/store/contexts';
import { ArticleDataBySlugView, ArticleDataView } from 'client/data-explorers/article-data/components';
import { DataExplorerView } from 'client/data-explorers/layouts';
import AppStateProvider from 'client/data-explorers/store/AppStateProvider';

function BaseDataExplorer({ initialPageData }: { initialPageData: InitialArticleDataBySlugPageData }) {
    const state = useContext(BaseStateContext);

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
            ],
        },
    ]);

    const pageData = (initialPageData.data || state.pageData) as InitialArticleDataBySlugPageData['data'];

    console.log('data-explorers - BaseDataExplorer', { initialPageData, state, pageData });
    return (
        <BasePage>
            <AppStateProvider initialState={initialPageData}>
                <RouterProvider router={browserRouter} />
            </AppStateProvider>
        </BasePage>
    );
}

export default BaseDataExplorer;

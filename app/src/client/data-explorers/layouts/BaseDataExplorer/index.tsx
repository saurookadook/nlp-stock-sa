import React from 'react';
import { RouterProvider } from 'react-router-dom';

import type { AbstractPageData } from '@nlpssa-app-types/common/main';
import { BasePage } from 'client/common/layouts';
import AppStateProvider from 'client/data-explorers/store/AppStateProvider';
import browserRouter from 'client/data-explorers/browserRouter';

function BaseDataExplorer({ initialPageData }: { initialPageData: AbstractPageData }) {
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

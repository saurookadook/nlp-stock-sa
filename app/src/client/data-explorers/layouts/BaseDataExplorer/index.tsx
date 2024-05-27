import React from 'react';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

import type { DataExplorersStore, GenericStateStore } from '@nlpssa-app-types/common/main';
import { BasePage } from 'client/common/layouts';
import AppStateProvider from 'client/data-explorers/store/AppStateProvider';
import { dataExplorersRoutes } from 'client/data-explorers/routes';

function BaseDataExplorer({ initialPageData }: { initialPageData: GenericStateStore<DataExplorersStore> }) {
    console.log('data-explorers - BaseDataExplorer', { initialPageData });
    const browserRouter = createBrowserRouter(dataExplorersRoutes);

    return (
        <BasePage>
            <AppStateProvider initialState={initialPageData}>
                <RouterProvider router={browserRouter} />
            </AppStateProvider>
        </BasePage>
    );
}

export default BaseDataExplorer;

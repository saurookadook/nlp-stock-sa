import React from 'react';
import { RouterProvider } from 'react-router-dom';

import type { DataExplorersStore, GenericStateStore } from '@nlpssa-app-types/common/main';
import { BasePage } from 'client/common/layouts';
import AppStateProvider from 'client/data-explorers/store/AppStateProvider';
import browserRouter from 'client/data-explorers/routes';

export default function BaseDataExplorer({
    initialPageData,
}: {
    initialPageData: GenericStateStore<DataExplorersStore>;
}) {
    console.log('data-explorers - BaseDataExplorer', { initialPageData });

    return (
        <BasePage>
            <AppStateProvider initialState={initialPageData}>
                <RouterProvider router={browserRouter} />
            </AppStateProvider>
        </BasePage>
    );
}

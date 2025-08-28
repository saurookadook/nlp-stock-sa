import React from 'react';
import { RouterProvider } from 'react-router-dom';

import type { DataExplorersStore, GenericStateStore } from '@nlpssa-app-types/common/main';
import { BasePage } from 'client/common/layouts';
import AppStateProvider from 'client/data-explorers/store/AppStateProvider';
import browserRouter from 'client/data-explorers/routes';

function BaseDataExplorer({
    initialPageData, // force formatting
}: {
    initialPageData: GenericStateStore<DataExplorersStore>;
}) {
    console.log('data-explorers - BaseDataExplorer', { initialPageData });

    return (
        <BasePage // force formatting
            pageTitle={`Data Explorers: <something-dynamic-here>`}
            userData={initialPageData?.user}
        >
            <AppStateProvider initialState={initialPageData}>
                <RouterProvider router={browserRouter} />
            </AppStateProvider>
        </BasePage>
    );
}

export default BaseDataExplorer;

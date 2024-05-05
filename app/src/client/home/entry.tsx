// import '@nlpssa-app-types/common';
import React from 'react';
import { createRoot } from 'react-dom/client';

import { AmbiguousObject } from '@nlpssa-app-types/common/main';
import { App } from 'client/home/components';
import AppStateProvider from 'client/home/store/AppStateProvider';
// import reportWebVitals from 'client/reportWebVitals';

window.renderApp = async (initialPageData) => {
    const root = createRoot(document.getElementById('nlpssa-main'));
    console.log('renderApp - initialPageData: ', { initialPageData });

    root.render(
        <React.StrictMode>
            <AppStateProvider>
                <App initialPageData={initialPageData as { data: AmbiguousObject[] }} />
            </AppStateProvider>
        </React.StrictMode>,
    );
};

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();

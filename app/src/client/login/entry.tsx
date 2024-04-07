import '@nlpssa-app-types/common';
import React from 'react';
import { createRoot } from 'react-dom/client';

import { App } from 'client/login/components';
// import reportWebVitals from 'client/reportWebVitals';

window.renderApp = async (initialPageData) => {
    const root = createRoot(document.getElementById('nlpssa-main'));

    root.render(
        <React.StrictMode>
            <App data={initialPageData} />
        </React.StrictMode>,
    );
};

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();

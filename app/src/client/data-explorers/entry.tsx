import React from 'react';
import { createRoot } from 'react-dom/client';
import { ChakraProvider, ColorModeScript, extendTheme } from '@chakra-ui/react';

import type { DataExplorersStore } from '@nlpssa-app-types/common/main';
import { BaseDataExplorer } from 'client/data-explorers/layouts';
import { AppStateProvider } from 'client/data-explorers/store';
// import reportWebVitals from 'client/reportWebVitals';
import { cleanAndTransformSentimentAnalyses } from 'client/data-explorers/utils/dataNormalizers';

window.renderApp = async (data) => {
    const initialPageData = data as DataExplorersStore;
    const root = createRoot(document.getElementById('nlpssa-main'));
    console.log({ page: 'data-explorers', initialPageData });

    const theme = extendTheme({
        initialColorMode: 'system',
        useSystemColorMode: true,
    });

    // TODO: make this less ugly?
    if (initialPageData.sentimentAnalysesBySlug != null) {
        const { sentimentAnalyses } = initialPageData.sentimentAnalysesBySlug;
        initialPageData.sentimentAnalysesBySlug.sentimentAnalyses =
            cleanAndTransformSentimentAnalyses(sentimentAnalyses);
    }

    root.render(
        <AppStateProvider initialState={initialPageData}>
            <ChakraProvider theme={theme}>
                <ColorModeScript initialColorMode={theme.config.initialColorMode} />

                <BaseDataExplorer />
            </ChakraProvider>
        </AppStateProvider>,
    );
};

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();

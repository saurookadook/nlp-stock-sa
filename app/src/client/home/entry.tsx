import React from 'react';
import { createRoot } from 'react-dom/client';
import { ChakraProvider, ColorModeScript, extendTheme } from '@chakra-ui/react';

import type { InitialHomePageData } from '@nlpssa-app-types/common/main';
import { HomeApp } from 'client/home/components';
import AppStateProvider from 'client/home/store/AppStateProvider';
// import reportWebVitals from 'client/reportWebVitals';

window.renderApp = async (initialPageData) => {
    const root = createRoot(document.getElementById('nlpssa-main'));
    console.log('renderApp - initialPageData: ', { initialPageData });

    const theme = extendTheme({
        initialColorMode: 'system',
        useSystemColorMode: true,
    });

    root.render(
        <AppStateProvider>
            <ChakraProvider theme={theme}>
                <ColorModeScript initialColorMode={theme.config.initialColorMode} />
                <HomeApp initialPageData={initialPageData as InitialHomePageData} />
            </ChakraProvider>
        </AppStateProvider>,
    );
};

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();

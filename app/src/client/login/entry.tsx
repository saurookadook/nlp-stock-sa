import React from 'react';
import { createRoot } from 'react-dom/client';
import { ChakraProvider, ColorModeScript, extendTheme } from '@chakra-ui/react';

import { LoginApp } from 'client/login/components';
// import reportWebVitals from 'client/reportWebVitals';

window.renderApp = async (initialPageData) => {
    const root = createRoot(document.getElementById('nlpssa-main'));
    console.log({ page: 'login', initialPageData });

    const theme = extendTheme({
        initialColorMode: 'system',
        useSystemColorMode: true,
    });

    root.render(
        <ChakraProvider theme={theme}>
            <ColorModeScript initialColorMode={theme.config.initialColorMode} />
            <LoginApp initialPageData={initialPageData} />
        </ChakraProvider>,
    );
};

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();

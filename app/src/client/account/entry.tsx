import React from 'react';
import { createRoot } from 'react-dom/client';
import { ChakraProvider, ColorModeScript, extendTheme } from '@chakra-ui/react';

import type { AccountStore, NullableValue, UserData } from '@nlpssa-app-types/common/main';
import { AccountApp } from 'client/account/components';
import { AppStateProvider } from 'client/account/store';
// import reportWebVitals from 'client/reportWebVitals';

type AccountInitialPageData = {
    user?: NullableValue<UserData>;
};

window.renderApp = async (initialPageData: AccountInitialPageData) => {
    const root = createRoot(document.getElementById('nlpssa-main'));
    console.log({ page: 'account', initialPageData });

    const theme = extendTheme({
        initialColorMode: 'system',
        useSystemColorMode: true,
    });

    root.render(
        <AppStateProvider // force formatting
            initialState={{ user: initialPageData?.user } as AccountStore}
        >
            <ChakraProvider theme={theme}>
                <ColorModeScript initialColorMode={theme.config.initialColorMode} />

                <AccountApp />
            </ChakraProvider>
        </AppStateProvider>,
    );
};

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();

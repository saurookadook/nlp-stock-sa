import React from 'react';
import { ChakraProvider, ColorModeScript, extendTheme } from '@chakra-ui/react';
import type { Preview } from '@storybook/react';

const theme = extendTheme({
    initialColorMode: 'system',
    useSystemColorMode: true,
});

const ChakraThemeDecorator = (Story) => (
    <ChakraProvider>
        <ColorModeScript initialColorMode={theme.config.initialColorMode} />
        <Story />
    </ChakraProvider>
);

const preview: Preview = {
    decorators: [ChakraThemeDecorator],
    parameters: {
        controls: {
            matchers: {
                color: /(background|color)$/i,
                date: /Date$/i,
            },
        },
    },
};

export default preview;

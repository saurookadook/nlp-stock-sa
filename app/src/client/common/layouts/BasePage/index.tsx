import React from 'react';
import { Box, Heading } from '@chakra-ui/react';

import { NavHeader } from 'client/common/components';

function BasePage({ pageTitle, children }: React.PropsWithChildren<{ pageTitle?: string | JSX.Element }>) {
    return (
        <Box>
            <NavHeader />
            <Box as="section" display="flex" flexDirection="column" paddingY="1rem">
                <Heading marginY="0.5rem" textAlign="center">
                    {pageTitle || `💸 🤑 💸 THE MONEY MAKERRRRR 💸 🤑 💸 `}
                </Heading>
                {children}
            </Box>
        </Box>
    );
}

export default BasePage;

import React from 'react';
import { Box } from '@chakra-ui/react';

import { NavHeader } from 'client/common/components';

function BasePage({ pageTitle, children }: React.PropsWithChildren<{ pageTitle?: string }>) {
    return (
        <Box>
            <NavHeader />
            <Box as="section">
                <h1>{pageTitle || `💸 🤑 💸 THE MONEY MAKERRRRR 💸 🤑 💸 `}</h1>
                {children}
            </Box>
        </Box>
    );
}

export default BasePage;

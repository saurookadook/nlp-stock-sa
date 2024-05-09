import React, { MouseEventHandler } from 'react';
import { Box, Button, Heading, useColorMode } from '@chakra-ui/react';
import { MoonIcon, SunIcon } from '@chakra-ui/icons';

import { NavHeader } from 'client/common/components';

function BasePage({
    headingChildren,
    pageTitle,
    children,
}: React.PropsWithChildren<{ headingChildren?: React.ReactNode; pageTitle?: string | JSX.Element }>) {
    const { colorMode, toggleColorMode } = useColorMode();

    const prompts = [
        'Are you sure?',
        "Are you sure you're sure?",
        "Are you sure you're sure you're sure?",
        'Are you sure now?',
    ];
    function annoyingClickHandler(e: MouseEventHandler) {
        const random = (Math.ceil(Math.random() * 4) || 1) - 1;
        console.log(`random: ${random}`);
        if (window.confirm(prompts[random])) {
            return window.alert('Join the club 🫠');
        }

        return annoyingClickHandler(e);
    }

    return (
        <Box>
            <NavHeader>
                {headingChildren}
                <Button colorScheme="teal" marginLeft="1rem" onClick={annoyingClickHandler}>
                    Want&nbsp;free&nbsp;Money? Click&nbsp;Me!
                </Button>
                <Button marginLeft="1rem" onClick={toggleColorMode}>
                    {colorMode === 'light' ? <SunIcon /> : <MoonIcon />}
                </Button>
            </NavHeader>
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

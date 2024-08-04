import React from 'react';
import { Box, Button, Heading, Spacer, useColorMode } from '@chakra-ui/react';
import { MoonIcon, SunIcon } from '@chakra-ui/icons';

import { NavHeader } from 'client/common/components';

function BasePage({
    headingChildren, // force formatting
    children,
    pageTitle,
    ...props
}: React.PropsWithChildren<{ headingChildren?: React.ReactNode; pageTitle?: string | JSX.Element }> & {
    className?: string; // TODO: there must be a better way to fix this type issue
}) {
    const { colorMode, toggleColorMode } = useColorMode();

    const prompts = [
        'Are you sure?',
        "Are you sure you're sure?",
        "Are you sure you're sure you're sure?",
        'Are you sure now?',
    ];

    function annoyingClickHandler(e) {
        const random = (Math.ceil(Math.random() * 4) || 1) - 1;
        console.log(`random: ${random}`);
        if (window.confirm(prompts[random])) {
            return window.alert('Join the club 🫠');
        }

        return annoyingClickHandler(e);
    }

    return (
        <Box {...props}>
            <NavHeader>
                <Spacer />
                {headingChildren}
                <Button colorScheme="teal" marginLeft="1rem" onClick={annoyingClickHandler}>
                    Want&nbsp;free&nbsp;Money? Click&nbsp;Me!
                </Button>
                <Button marginLeft="1rem" onClick={toggleColorMode}>
                    {colorMode === 'light' ? <SunIcon /> : <MoonIcon />}
                </Button>
            </NavHeader>
            <Box as="section" display="flex" flexDirection="column" paddingY="1rem">
                {pageTitle != null && (
                    <Heading marginTop="0.5rem" marginBottom="1rem" textAlign="center">
                        {pageTitle}
                    </Heading>
                )}
                {children}
            </Box>
        </Box>
    );
}

export default BasePage;

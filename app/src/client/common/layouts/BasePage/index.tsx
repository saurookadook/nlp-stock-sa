import React from 'react';
import { Box, Button, Heading, Spacer, useColorMode } from '@chakra-ui/react';
import { MoonIcon, SunIcon } from '@chakra-ui/icons';

import type { NullableValue, UserData } from '@nlpssa-app-types/common/main';
import { NavHeader, UserAvatarMenu } from 'client/common/components';

type BasePageProps = React.PropsWithChildren<{
    className?: string;
    headingChildren?: React.ReactNode;
    pageTitle?: string | JSX.Element;
    userData?: NullableValue<UserData>;
}>;

function BasePage({
    children,
    headingChildren, // force formatting
    pageTitle,
    userData,
    ...props
}: BasePageProps) {
    const { colorMode, toggleColorMode } = useColorMode();

    const prompts = [
        'Are you sure?',
        "Are you sure you're sure?",
        "Are you sure you're sure you're sure?",
        'Are you sure now?',
    ];

    function annoyingClickHandler(e: React.MouseEvent<HTMLButtonElement>) {
        const random = (Math.ceil(Math.random() * 4) || 1) - 1;
        console.log(`random: ${random}`);
        if (window.confirm(prompts[random])) {
            return window.alert('Join the club 🫠');
        }

        return annoyingClickHandler(e);
    }

    console.log(
        JSON.parse(
            JSON.stringify({
                name: BasePage.name,
                userData: userData,
            }),
        ),
    );

    return (
        <Box {...props}>
            <NavHeader>
                <Spacer />

                {headingChildren}

                <Button colorScheme="teal" onClick={annoyingClickHandler}>
                    Want&nbsp;free&nbsp;Money? Click&nbsp;Me!
                </Button>

                <Button
                    onClick={toggleColorMode} // force formatting
                >
                    {colorMode === 'light' ? <SunIcon /> : <MoonIcon />}
                </Button>

                <UserAvatarMenu username={userData?.username} />
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

import React, { useEffect, useState } from 'react';
import { Box, Center, Container, Spacer, Spinner } from '@chakra-ui/react';

import type { AmbiguousObject } from '@nlpssa-app-types/common/main';
import { BasePage } from 'client/common/layouts';
import { AppleLinkBox, GitHubLinkBox, GoogleLinkBox, MicrosoftLinkBox } from 'client/login/components';

function LoginApp({ initialPageData }: { initialPageData?: Record<string, unknown> | null }) {
    console.log('login - LoginApp', { initialPageData });

    const [loginData, setLoginData] = useState({ ...initialPageData } || {} as AmbiguousObject);

    const isLoginDataLoaded = () => Object.keys(loginData).length > 0;

    useEffect(() => {
        if (!isLoginDataLoaded()) {
            fetch('/api/auth/login')
                .then((resp) => {
                    try {
                        return resp.json();
                    } catch (e) {
                        return resp.text();
                    }
                })
                .then((jresp) => {
                    setLoginData(jresp);
                })
                .catch((e) => console.error(e));
        }
    }, []);

    const sharedLinkBoxProps = {
        as: 'button',
        borderRadius: '5px',
        display: 'flex',
        justifyContent: 'space-around',
        paddingY: '1rem',
        paddingX: '2rem',
    };

    return (
        <BasePage // force formatting
            className="App"
            headingChildren={<Spacer />}
            pageTitle={<span>{`💸 Login 💸`}</span>}
        >
            <Container className="home" margin="0 auto" maxWidth="40rem">
                <Center
                    borderColor="gray.400"
                    borderRadius="5px"
                    borderStyle="solid"
                    borderWidth="1px"
                    flexDirection="column"
                    // h="50vh"
                    minHeight="75vh"
                    w="100%"
                >
                    {isLoginDataLoaded() ? (
                        <Box display="flex" flexDirection="column" rowGap="1rem">
                            <AppleLinkBox href={'#'} {...sharedLinkBoxProps} />
                            <GitHubLinkBox href={loginData.githubUrl} {...sharedLinkBoxProps} />
                            <GoogleLinkBox href={'#'} {...sharedLinkBoxProps} />
                            <MicrosoftLinkBox href={'#'} {...sharedLinkBoxProps} />
                        </Box>
                    ) : (
                        <Spinner // force formatting
                            color="teal"
                            emptyColor="gray.200"
                            size="xl"
                            speed="0.65s"
                            thickness="4px"
                        />
                    )}
                </Center>
            </Container>
        </BasePage>
    );
}

export default LoginApp;

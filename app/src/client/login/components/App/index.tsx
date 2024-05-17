import React, { useEffect, useState } from 'react';
import { Center, Container, LinkBox, LinkOverlay, Spacer, Spinner } from '@chakra-ui/react';

import type { AmbiguousObject } from '@nlpssa-app-types/common/main';
// import { BaseLink } from 'client/common/components';
import { BasePage } from 'client/common/layouts';

function App({ initialPageData }: { initialPageData?: Record<string, unknown> | null }) {
    console.log('login - App', { initialPageData });

    const [loginData, setLoginData] = useState({} as AmbiguousObject);

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
                        <LinkBox
                            as="button"
                            backgroundColor="blackAlpha.800"
                            borderRadius="5px"
                            color="white"
                            paddingY="0.5rem"
                            paddingX="1rem"
                        >
                            <LinkOverlay href={loginData.githubUrl as string}>Log in with GitHub</LinkOverlay>
                        </LinkBox>
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

export default App;

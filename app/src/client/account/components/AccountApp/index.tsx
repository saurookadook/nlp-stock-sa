import React, { useEffect, useState } from 'react';
import { Box, Center, Container, Spacer, Spinner } from '@chakra-ui/react';

import type { AmbiguousObject, NullableValue, UserData } from '@nlpssa-app-types/common/main';
import { BasePage } from 'client/common/layouts';

type AccountAppProps = {
    initialPageData: {
        user?: NullableValue<UserData>;
    };
};

function AccountApp({ initialPageData }: AccountAppProps) {
    console.log('account - AccountApp', { initialPageData });

    const [accountData, setAccountData] = useState({ ...initialPageData } as AmbiguousObject);

    const isAccountDataLoaded = () => Object.keys(accountData).length > 0;

    return (
        <BasePage // force formatting
            className="App"
            headingChildren={<Spacer />}
            pageTitle={<span>{`💸 Login 💸`}</span>}
            userData={initialPageData?.user}
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
                    {isAccountDataLoaded() ? (
                        <Box display="flex" flexDirection="column" rowGap="1rem">
                            <pre>
                                <code>{JSON.stringify(accountData, null, 2)}</code>
                            </pre>
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

export default AccountApp;

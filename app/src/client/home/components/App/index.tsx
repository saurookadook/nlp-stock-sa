import React from 'react';
import { Center, ChakraProvider, Container } from '@chakra-ui/react';
// import logo from '/logo.svg';

function App({ data }: { data?: Record<string, unknown> | null }) {
    console.log('home - App', { data });
    return (
        <ChakraProvider>
            <Container className="home" maxWidth="75vw">
                <Center
                    borderColor="gray.400"
                    borderRadius="5px"
                    borderStyle="solid"
                    borderWidth="1px"
                    flexDirection="column"
                    h="50vh"
                    w="50vw"
                >
                    <header className="home-header">{`💸 🤑 💸 Welcome to NLP SSA 💸 🤑 💸`}</header>
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <p>
                            <em>{`a.k.a.`}</em>
                        </p>
                        <p>
                            <b>{`💸 🤑 💸 THE MONEY MAKERRRRR 💸 🤑 💸 `}</b>
                        </p>
                    </div>
                </Center>
            </Container>
        </ChakraProvider>
    );
}

export default App;

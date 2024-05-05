import React, { useContext, useEffect } from 'react';
import { Center, ChakraProvider, Container } from '@chakra-ui/react';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { fetchArticleData } from 'client/home/store/actions';
// import logo from '/logo.svg';

interface InitialPageData {
    data: Record<string, unknown>[] | null;
}

function App({ initialPageData }: { initialPageData: InitialPageData }) {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);

    const { data: pageData } = initialPageData;

    useEffect(() => {
        if (pageData == null) {
            window.$fetchArticle = fetchArticleData;
        }

        if (state.pageData == null) {
            fetchArticleData({ dispatch });
        }
    });
    console.log('home - App', { initialPageData });
    return (
        <ChakraProvider>
            <Container className="home" marginX="auto" maxWidth="75vw">
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
                    <section>
                        <h1>Home: Article Data</h1>
                        {pageData != null && pageData.length > 0 ? (
                            <ul>
                                {pageData.map((record, i) => (
                                    <li key={`data-record-${i}`}>
                                        <details>
                                            <summary>
                                                Stock: {record.quoteStockSymbol}, URL: {record.sourceUrl}
                                            </summary>
                                            <div>{record.rawContent}</div>
                                            <div>{record.sentenceTokens}</div>
                                        </details>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            'No data :['
                        )}
                    </section>
                </Center>
            </Container>
        </ChakraProvider>
    );
}

export default App;

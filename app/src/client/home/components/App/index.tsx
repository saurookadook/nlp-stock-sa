import React, { useContext, useEffect } from 'react';
import { Center, ChakraProvider, Container } from '@chakra-ui/react';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { fetchArticleData } from 'client/home/store/actions';
// import logo from '/logo.svg';

type PageData = Record<string, unknown>[];

interface InitialPageData {
    data: PageData | null;
}

function App({ initialPageData }: { initialPageData: InitialPageData }): React.ReactElement {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);

    const pageData = initialPageData.data || state.pageData;

    useEffect(() => {
        if (state.pageData == null) {
            fetchArticleData({ dispatch });
        }
    });
    console.log('home - App', { initialPageData, pageData });
    return (
        <ChakraProvider>
            <Container className="home" style={{ margin: '0 auto' }} maxWidth="75vw">
                <Center
                    borderColor="gray.400"
                    borderRadius="5px"
                    borderStyle="solid"
                    borderWidth="1px"
                    flexDirection="column"
                    // h="50vh"
                    w="100%"
                >
                    <header
                        className="home-header"
                        style={{ fontSize: '2rem', fontWeight: '700' }}
                    >{`💸 🤑 💸 Welcome to NLP SSA 💸 🤑 💸`}</header>
                    <div style={{ display: 'flex', flexDirection: 'column', textAlign: 'center' }}>
                        <p>
                            <em>{`a.k.a.`}</em>
                        </p>
                        <p>
                            <b>{`💸 🤑 💸 THE MONEY MAKERRRRR 💸 🤑 💸 `}</b>
                        </p>
                    </div>
                    <section>
                        <h1>
                            <b>Home</b>: Article Data
                        </h1>
                        {pageData != null && (pageData as PageData).length > 0 ? (
                            <ul>
                                {(pageData as PageData).map((record, i) => (
                                    <li key={`data-record-${i}`} style={{ listStyle: 'none' }}>
                                        <details>
                                            <summary>
                                                <b>Stock</b>: {record.quoteStockSymbol}, <b>URL</b>:{' '}
                                                <a
                                                    href={record.sourceUrl as string}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                >
                                                    {record.sourceUrl}
                                                </a>
                                            </summary>
                                            <div
                                                style={{
                                                    alignItems: 'flex-start',
                                                    display: 'flex',
                                                    flexDirection: 'row',
                                                    justifyContent: 'space-evenly',
                                                    width: '100%',
                                                }}
                                            >
                                                <div
                                                    style={{
                                                        display: 'inline-flex',
                                                        flexDirection: 'column',
                                                        maxWidth: '45%',
                                                    }}
                                                >
                                                    <h2 style={{ fontWeight: 'bold' }}>Raw Content</h2>
                                                    <span>{record.rawContent}</span>
                                                </div>
                                                <div
                                                    style={{
                                                        display: 'inline-flex',
                                                        flexDirection: 'column',
                                                        maxWidth: '45%',
                                                    }}
                                                >
                                                    <h2 style={{ fontWeight: 'bold' }}>Sentence Tokens</h2>
                                                    <span>{record.sentenceTokens}</span>
                                                </div>
                                            </div>
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

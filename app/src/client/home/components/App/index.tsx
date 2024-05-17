import React, { useContext, useEffect } from 'react';
import { Box, Button, Center, Container, Flex, Heading, Spacer } from '@chakra-ui/react';

import type { GroupedArticleData } from '@nlpssa-app-types/common/main';
import { BaseLink } from 'client/common/components';
import { BasePage } from 'client/common/layouts';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { ArticleDataList } from 'client/home/components';
import { fetchArticleData } from 'client/home/store/actions';

type PageData = GroupedArticleData[] | null;

interface InitialPageData {
    data: PageData;
}

function StockArticleDataGroup({ quoteStockSymbol, articleData }) {
    return (
        <Box>
            <Heading backgroundColor="teal" color="white" padding="0.5rem 1rem">
                <Box as="span" fontWeight="700">
                    {quoteStockSymbol}
                </Box>
            </Heading>
            <ArticleDataList articleData={articleData} />
        </Box>
    );
}

function App({ initialPageData }: { initialPageData: InitialPageData }): React.ReactElement {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);

    const pageData = (initialPageData.data || state.pageData) as PageData;

    useEffect(() => {
        if (state.pageData == null) {
            fetchArticleData({ dispatch });
        }
    });

    console.log('home - App', { initialPageData, pageData });
    return (
        <BasePage
            headingChildren={
                <>
                    <Spacer />
                    <BaseLink href="/">Home</BaseLink>
                    <Button>I&nbsp;AM BUTTON</Button>
                </>
            }
            pageTitle={
                <span>
                    <b>Home</b>: Article Data
                </span>
            }
        >
            <Container className="home" style={{ margin: '0 auto' }} maxWidth="75vw">
                <Center
                    borderColor="gray.400"
                    borderRadius="5px"
                    borderStyle="solid"
                    borderTopWidth="0px"
                    borderRightWidth="1px"
                    borderBottomWidth="0px"
                    borderLeftWidth="1px"
                    flexDirection="column"
                    // h="50vh"
                    w="100%"
                >
                    <Flex className="article-data-list-wrapper" alignSelf="stretch" flexDirection="column">
                        {pageData != null && pageData.length > 0
                            ? pageData.map((groupedData, i) => {
                                  const { quoteStockSymbol, articleData } = groupedData;
                                  return (
                                      <StockArticleDataGroup
                                          key={`${quoteStockSymbol}-${i}`}
                                          quoteStockSymbol={quoteStockSymbol}
                                          articleData={articleData}
                                      />
                                  );
                              })
                            : 'No data :['}
                    </Flex>
                </Center>
            </Container>
        </BasePage>
    );
}

export default App;

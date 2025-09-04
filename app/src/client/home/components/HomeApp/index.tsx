import React, { useContext, useEffect } from 'react';
import { Button, Center, Container, Flex } from '@chakra-ui/react';

import type { HomeStore } from '@nlpssa-app-types/common/main';
import { NoDataMessage, StockArticleDataGroup } from 'client/common/components';
import { BasePage } from 'client/common/layouts';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { fetchArticleData } from 'client/home/store/actions';

function HomeApp(): React.ReactElement {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);

    const { pageData, user } = state as HomeStore;

    useEffect(() => {
        if (state.pageData == null) {
            fetchArticleData({ dispatch });
        }
    });

    console.log('home - HomeApp', { state, pageData });
    return (
        <BasePage
            appDispatch={dispatch}
            headingChildren={<Button>I&nbsp;AM BUTTON</Button>}
            pageTitle={
                <span>
                    <b>Home</b>: Article Data
                </span>
            }
            userData={user}
        >
            <Container className="home" margin="0 auto" maxWidth="75vw">
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
                        {pageData != null && pageData.length > 0 ? (
                            pageData.map((groupedData, i) => {
                                const { quoteStockSymbol, articleData } = groupedData;
                                return (
                                    <StockArticleDataGroup
                                        key={`${quoteStockSymbol}-${i}`}
                                        quoteStockSymbol={quoteStockSymbol}
                                        articleData={articleData}
                                    />
                                );
                            })
                        ) : (
                            <NoDataMessage />
                        )}
                    </Flex>
                </Center>
            </Container>
        </BasePage>
    );
}

export default HomeApp;

import React, { useContext, useEffect } from 'react';
import { Center, Container, Flex } from '@chakra-ui/react';

import type { InitialArticleDataBySlugPageData } from '@nlpssa-app-types/common/main';
import { StockArticleDataGroup } from 'client/common/components';
import { BasePage } from 'client/common/layouts';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { fetchArticleDataByStockSlug } from 'client/data-explorers/store/actions';

function ArticleDataApp({
    initialPageData,
    stockSlug,
}: {
    initialPageData: InitialArticleDataBySlugPageData;
    stockSlug: string;
}) {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);

    const pageData = (initialPageData.data || state.pageData) as InitialArticleDataBySlugPageData['data'];

    useEffect(() => {
        if (state.pageData == null) {
            fetchArticleDataByStockSlug({ dispatch, stockSlug });
        }
    });

    console.log('article-data - ArticleDataApp', { initialPageData, state, pageData });
    return (
        <BasePage>
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
                        {pageData != null ? (
                            <StockArticleDataGroup
                                quoteStockSymbol={pageData.quoteStockSymbol}
                                articleData={pageData.articleData}
                            />
                        ) : (
                            'No data :['
                        )}
                    </Flex>
                </Center>
            </Container>
        </BasePage>
    );
}

export default ArticleDataApp;

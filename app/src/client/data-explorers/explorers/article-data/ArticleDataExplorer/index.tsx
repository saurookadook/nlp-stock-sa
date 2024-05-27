import React, { useContext, useEffect } from 'react';
import { Flex } from '@chakra-ui/react';

import { type DataExplorersStore } from '@nlpssa-app-types/common/main';
import { NoDataMessage, StockArticleDataGroup } from 'client/common/components';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { fetchAllArticleData } from 'client/data-explorers/store/actions';

function ArticleDataExplorer() {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);

    const { articleData } = state as DataExplorersStore;

    useEffect(() => {
        if (state.pageData == null) {
            fetchAllArticleData({ dispatch });
        }
    });

    console.log('data-explorers.article-data - ArticleDataExplorer', { state, articleData });
    return (
        <Flex className="article-data-list-wrapper" alignSelf="stretch" flexDirection="column">
            {articleData != null && articleData.length > 0 ? (
                articleData.map((groupedData, i) => {
                    const { quoteStockSymbol, articleData } = groupedData;
                    return (
                        <StockArticleDataGroup
                            key={`${quoteStockSymbol}-${i}`}
                            articleData={articleData}
                            quoteStockSymbol={quoteStockSymbol}
                            routerDomAware={true}
                        />
                    );
                })
            ) : (
                <NoDataMessage />
            )}
        </Flex>
    );
}

export default ArticleDataExplorer;

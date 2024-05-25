import React, { useContext, useEffect } from 'react';
import { Flex } from '@chakra-ui/react';

import { type ArticleDataViewStore } from '@nlpssa-app-types/common/main';
import { StockArticleDataGroup } from 'client/common/components';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { fetchAllArticleData } from 'client/data-explorers/store/actions';

function ArticleDataView() {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);

    const pageData = (state as ArticleDataViewStore).pageData;

    useEffect(() => {
        if (state.pageData == null) {
            fetchAllArticleData({ dispatch });
        }
    });

    console.log('data-explorers.article-data - ArticleDataView', { state, pageData });
    return (
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
    );
}

export default ArticleDataView;

import React, { useContext, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Flex } from '@chakra-ui/react';

import { DataExplorersStore } from '@nlpssa-app-types/common/main';
import { StockArticleDataGroup } from 'client/common/components';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { fetchArticleDataByStockSlug } from 'client/data-explorers/store/actions';

function ArticleDataBySlugExplorer() {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);
    const params = useParams();

    const { articleDataBySlug } = state as DataExplorersStore;

    useEffect(() => {
        if (articleDataBySlug == null) {
            fetchArticleDataByStockSlug({ dispatch, stockSlug: params.stockSlug });
        }
    }, [params.stockSlug]);

    console.log('data-explorers.article-data - ArticleDataBySlugExplorer', { state });
    return (
        <Flex className="article-data-list-wrapper" alignSelf="stretch" flexDirection="column">
            {articleDataBySlug != null ? (
                <StockArticleDataGroup
                    quoteStockSymbol={articleDataBySlug.quoteStockSymbol}
                    articleData={articleDataBySlug.articleData}
                />
            ) : (
                'No data :['
            )}
        </Flex>
    );
}

export default ArticleDataBySlugExplorer;

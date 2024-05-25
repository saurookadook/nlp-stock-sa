import React, { useContext, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Flex } from '@chakra-ui/react';

import type { InitialArticleDataBySlugPageData } from '@nlpssa-app-types/common/main';
import { StockArticleDataGroup } from 'client/common/components';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { fetchArticleDataByStockSlug } from 'client/data-explorers/store/actions';

function ArticleDataBySlugView() {
    // const location = useLocation();
    const params = useParams();
    // TODO: maybe use `useMemo`?
    // const stockSlug = location.pathname.replace(/^\/\S+\/(?=[^\/]+$)/gim, '');

    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);

    const pageData = state.pageData as InitialArticleDataBySlugPageData['data'];

    useEffect(() => {
        if (state.pageData == null) {
            fetchArticleDataByStockSlug({ dispatch, stockSlug: params.stockSlug });
        }
    });

    console.log('data-explorers.article-data - ArticleDataBySlugView', { state, pageData });
    return (
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
    );
}

export default ArticleDataBySlugView;

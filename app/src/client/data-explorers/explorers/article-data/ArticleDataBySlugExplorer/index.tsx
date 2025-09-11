import React, { useContext, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Flex } from '@chakra-ui/react';

import { DataExplorersStore } from '@nlpssa-app-types/common/main';
import { NoDataMessage, StockArticleDataGroup } from 'client/common/components';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { usePrevious } from 'client/common/utils';
import { fetchArticleDataByStockSlug } from 'client/data-explorers/store/actions';

function ArticleDataBySlugExplorer({ dataListOnly = false }) {
  const state = useContext(BaseStateContext);
  const dispatch = useContext(BaseDispatchContext);
  const params = useParams();
  const previousStockSlug = usePrevious(params.stockSlug);

  const { articleDataBySlug } = state as DataExplorersStore;

  useEffect(() => {
    if (
      articleDataBySlug == null ||
      (previousStockSlug != null && previousStockSlug === params.stockSlug)
    ) {
      fetchArticleDataByStockSlug({ dispatch, stockSlug: params.stockSlug });
    }
  }, [params.stockSlug]);

  console.log('data-explorers.article-data - ArticleDataBySlugExplorer', { state });
  return (
    <Flex
      className="article-data-list-wrapper"
      alignSelf="stretch"
      flexDirection="column"
    >
      {articleDataBySlug != null ? (
        <StockArticleDataGroup
          articleData={articleDataBySlug.articleData}
          dataListOnly={dataListOnly}
          quoteStockSymbol={articleDataBySlug.quoteStockSymbol}
          routerDomAware={true}
        />
      ) : (
        <NoDataMessage />
      )}
    </Flex>
  );
}

export default ArticleDataBySlugExplorer;

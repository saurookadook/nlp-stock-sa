import React from 'react';
import { Box, Heading, Link, Spacer } from '@chakra-ui/react';

import { ArticleDataList } from 'client/common/components';

function StockArticleDataGroup({ quoteStockSymbol, articleData }) {
    return (
        <Box>
            <Heading alignItems="center" backgroundColor="teal" color="white" display="flex" padding="0.5rem 1rem">
                <Box as="span" fontWeight="700">
                    {quoteStockSymbol}
                </Box>
                <Spacer />
                <Link href={`/app/data-explorers/article-data/${quoteStockSymbol}`} fontSize="1rem">
                    See All
                </Link>
            </Heading>
            <ArticleDataList articleData={articleData} />
        </Box>
    );
}

export default StockArticleDataGroup;

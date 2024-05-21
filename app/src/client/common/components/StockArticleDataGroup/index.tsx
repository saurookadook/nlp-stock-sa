import React from 'react';
import { Box, Heading } from '@chakra-ui/react';

import { ArticleDataList } from 'client/common/components';

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

export default StockArticleDataGroup;

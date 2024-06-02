import React from 'react';
import { Link as RouterDomLink } from 'react-router-dom';
import {
    Box, // force formatting
    Heading,
    Link,
    Spacer,
    Text,
    useColorModeValue,
} from '@chakra-ui/react';
import { ArticleDataList } from 'client/common/components';

function StockArticleDataGroup({ articleData, quoteStockSymbol, routerDomAware = false }) {
    const headingBackgroundColor = useColorModeValue('teal.500', 'teal.200');
    const headingColor = useColorModeValue('white', 'gray.800');

    const seeAllTarget = `/app/data-explorers/article-data/${quoteStockSymbol}`;

    return (
        <Box id={`${quoteStockSymbol}-data-group`}>
            <Heading
                alignItems="center" // force formatting
                backgroundColor={headingBackgroundColor}
                color={headingColor}
                colorScheme="teal"
                display="flex"
                padding="0.5rem 1rem"
            >
                <Box as="span" fontWeight="700" className="quote-stock-symbol">
                    {quoteStockSymbol}
                </Box>
                <Spacer />
                <Text as="span" fontSize="1rem">
                    {routerDomAware ? (
                        <RouterDomLink to={seeAllTarget} className="router-dom-link">
                            See All
                        </RouterDomLink>
                    ) : (
                        <Link href={seeAllTarget} className="chakra-ui-link">
                            See All
                        </Link>
                    )}
                </Text>
            </Heading>
            <ArticleDataList articleData={articleData} />
        </Box>
    );
}

export default StockArticleDataGroup;

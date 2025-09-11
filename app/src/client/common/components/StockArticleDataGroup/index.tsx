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

function StockArticleDataGroup({
  articleData,
  dataListOnly = false,
  quoteStockSymbol,
  routerDomAware = false,
}) {
  const headingBackgroundColor = useColorModeValue('teal.500', 'teal.200');
  const headingColor = useColorModeValue('white', 'gray.800');

  const sentimentAnalysesTarget = `/app/data-explorers/sentiment-analyses/${quoteStockSymbol}`;
  const seeAllTarget = `/app/data-explorers/article-data/${quoteStockSymbol}`;

  const LinkComponent = routerDomAware ? RouterDomLink : Link;
  const linkConfigs = routerDomAware
    ? [
        {
          props: { className: 'router-dom-link', to: sentimentAnalysesTarget },
          text: 'View Sentiment Analysis',
        },
        {
          props: { className: 'router-dom-link', to: seeAllTarget },
          text: 'See All',
        },
      ]
    : [
        {
          props: { className: 'chakra-ui-link', href: sentimentAnalysesTarget },
          text: 'View Sentiment Analysis',
        },
        {
          props: { className: 'chakra-ui-link', href: seeAllTarget },
          text: 'See All',
        },
      ];

  return (
    <Box id={`${quoteStockSymbol}-data-group`}>
      {!dataListOnly && (
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

          {linkConfigs.map((linkConfig, index) => (
            <Text
              key={`heading-link-${index}`}
              as="span"
              fontSize="1rem"
              paddingX="0.5rem"
            >
              <LinkComponent {...linkConfig.props}>{linkConfig.text}</LinkComponent>
            </Text>
          ))}
        </Heading>
      )}

      <ArticleDataList articleData={articleData} />
    </Box>
  );
}

export default StockArticleDataGroup;

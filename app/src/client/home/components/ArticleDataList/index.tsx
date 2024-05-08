import React from 'react';
import {
    Accordion, // force formatting
    AccordionItem,
    AccordionButton,
    AccordionPanel,
    AccordionIcon,
    Box,
    Flex,
    Heading,
    Spacer,
} from '@chakra-ui/react';

import type { ArticleDataEntry } from '@nlpssa-app-types/common/main';

function ArticleDataList({ articleData }: React.PropsWithChildren<{ articleData: ArticleDataEntry[] }>) {
    return (
        <Accordion allowMultiple allowToggle>
            {articleData.map((record, i) => (
                <AccordionItem key={`article-record-${i}`}>
                    <Heading>
                        <AccordionButton>
                            <Box as="span" display="inline-flex" marginRight="1rem" textAlign="left">
                                <b>Stock</b>: {record.quoteStockSymbol}
                            </Box>
                            <Box as="span" display="inline-flex" textAlign="left" whiteSpace="pre-wrap">
                                <b>Title</b>
                                {': '}
                                {/* TODO: replace with actual title lol */}
                                {record.sourceUrl
                                    .replace(/^https:\/\/finance.yahoo.com\/(news\/|m\/[^\/]+?[\/])|\.html$/gim, '')
                                    .replace(/-/g, ' ')
                                    .toUpperCase()}
                            </Box>
                            <Spacer />
                            <AccordionIcon />
                        </AccordionButton>
                    </Heading>
                    <AccordionPanel>
                        <Flex justifyContent="center" textAlign="center" whiteSpace="pre-wrap">
                            <b>URL</b>
                            {': '}
                            <a href={record.sourceUrl} target="_blank" rel="noopener noreferrer">
                                {record.sourceUrl}
                            </a>
                        </Flex>
                        <Flex // force formatting
                            alignItems="flex-start"
                            flexDirection="row"
                            justifyContent="space-evenly"
                            width="100%"
                        >
                            <Box // force formatting
                                display="inline-flex"
                                flexDirection="column"
                                maxWidth="45%"
                            >
                                <h2 style={{ fontWeight: 'bold' }}>Raw Content</h2>
                                <span>{record.rawContent}</span>
                            </Box>
                            <Box // force formatting
                                display="inline-flex"
                                flexDirection="column"
                                maxWidth="45%"
                            >
                                <h2 style={{ fontWeight: 'bold' }}>Raw Content</h2>
                                <span>{record.rawContent}</span>
                            </Box>
                        </Flex>
                    </AccordionPanel>
                </AccordionItem>
            ))}
        </Accordion>
    );
}

export default ArticleDataList;

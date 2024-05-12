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
    SimpleGrid,
    Spacer,
    Text,
} from '@chakra-ui/react';

import type { ArticleDataEntry } from '@nlpssa-app-types/common/main';
import { BaseLink } from 'client/common/components';
import { toTitleCase } from 'client/common/utils';

function getTitleWithFallback(articleRecordArg) {
    return (
        articleRecordArg.title ||
        articleRecordArg.sourceUrl
            .replace(/^https:\/\/finance.yahoo.com\/(news\/|m\/[^\/]+?[\/])|\.html$/gim, '')
            .replace(/-/g, ' ')
            .toUpperCase()
    );
}

function getMetadataLabelFromKey(metadataKey: string) {
    const key = metadataKey.replace(/Date$/i, '');
    return toTitleCase(key);
}

function ArticleAccordianHeading({ articleRecord }: React.PropsWithChildren<{ articleRecord: ArticleDataEntry }>) {
    return (
        <Heading>
            <AccordionButton>
                <Box as="span" fontWeight="700" display="inline-flex" textAlign="left" whiteSpace="pre-wrap">
                    {getTitleWithFallback(articleRecord)}
                </Box>
                <Spacer />
                <AccordionIcon />
            </AccordionButton>
        </Heading>
    );
}

function ArticleMetadata({ articleRecord }) {
    const metadataKeys = Object.keys(articleRecord).filter((key) => !/sourceUrl|rawContent|sentenceTokens/im.test(key));

    return (
        <SimpleGrid
            columns={2}
            borderBottom="1px solid"
            borderColor="gray.400"
            marginBottom="1rem"
            paddingBottom="1rem"
        >
            {metadataKeys.map((key, i) => {
                return (
                    articleRecord[key] && (
                        <Box key={`${key}-${i}`}>
                            <b>{getMetadataLabelFromKey(key)}</b>: {articleRecord[key]}
                        </Box>
                    )
                );
            })}
            <Box>
                <b>URL</b>
                {': '}
                <BaseLink color="teal" href={articleRecord.sourceUrl} isExternal rel="noopener noreferrer">
                    {articleRecord.sourceUrl}
                </BaseLink>
            </Box>
        </SimpleGrid>
    );
}

function ArticleAccordianPanel({ articleRecord }) {
    return (
        <AccordionPanel>
            <Flex flexDirection="column" justifyContent="center">
                <ArticleMetadata articleRecord={articleRecord} />
            </Flex>
            <Flex // force formatting
                alignItems="flex-start"
                flexDirection="row"
                justifyContent="space-evenly"
                width="100%"
            >
                <Box // force formatting
                    className="raw-content"
                    display="inline-flex"
                    flexDirection="column"
                    maxWidth="45%"
                >
                    <h2 style={{ fontWeight: 'bold' }}>Raw Content</h2>
                    <Text>{articleRecord.rawContent}</Text>
                </Box>
                <Box // force formatting
                    className="sentence-tokens"
                    display="inline-flex"
                    flexDirection="column"
                    maxWidth="45%"
                >
                    <h2 style={{ fontWeight: 'bold' }}>Sentence Tokens</h2>
                    <Text>{articleRecord.sentenceTokens}</Text>
                </Box>
            </Flex>
        </AccordionPanel>
    );
}

function ArticleDataListItem({ articleRecord }: React.PropsWithChildren<{ articleRecord: ArticleDataEntry }>) {
    return (
        <AccordionItem>
            <ArticleAccordianHeading articleRecord={articleRecord} />
            <ArticleAccordianPanel articleRecord={articleRecord} />
        </AccordionItem>
    );
}

function ArticleDataList({ articleData }: React.PropsWithChildren<{ articleData: ArticleDataEntry[] }>) {
    return (
        // TODO: maybe this should use `ul` and `li` elements?
        <Accordion allowMultiple>
            {articleData.map((record, i) => (
                <ArticleDataListItem key={`article-record-${i}`} articleRecord={record} />
            ))}
        </Accordion>
    );
}

export default ArticleDataList;

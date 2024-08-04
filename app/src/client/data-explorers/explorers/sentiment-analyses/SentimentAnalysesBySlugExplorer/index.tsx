import React, { useContext, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
    Flex, // force formatting
    Heading,
    Table,
    Thead,
    Tbody,
    Tfoot,
    Tr,
    Th,
    Td,
    TableCaption,
    TableContainer,
} from '@chakra-ui/react';

import { DataExplorersStore } from '@nlpssa-app-types/common/main';
import { MultiSeriesLineGraph, NoDataMessage } from 'client/common/components';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { usePrevious } from 'client/common/utils';
import { fetchSentimentAnalysesByStockSlug } from 'client/data-explorers/store/actions';

function SentimentAnalysesBySlugExplorer() {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);
    const params = useParams();
    const previousStockSlug = usePrevious(params.stockSlug);

    const { sentimentAnalysesBySlug } = state as DataExplorersStore;

    useEffect(() => {
        if (sentimentAnalysesBySlug == null || (previousStockSlug != null && previousStockSlug !== params.stockSlug)) {
            fetchSentimentAnalysesByStockSlug({ dispatch, stockSlug: params.stockSlug });
        }
    }, [params.stockSlug]);

    console.log('data-explorers.sentiment-analyses - SentimentAnalysesBySlugExplorer', { state });
    return (
        <Flex alignItems="center" alignSelf="start" flexDirection="column" minWidth="80%">
            <Heading>Sentiment Analysis for {params.stockSlug}</Heading>
            {(sentimentAnalysesBySlug || {}).sentimentAnalyses != null ? (
                <Flex alignItems="center" flexDirection="column">
                    <MultiSeriesLineGraph
                        sentimentAnalysesData={sentimentAnalysesBySlug.sentimentAnalyses}
                        width={16 * 70}
                    />
                    <TableContainer
                        className="sentiment-analyses-wrapper"
                        // alignSelf="stretch" flexDirection="column"
                        maxHeight="32rem"
                        overflowY="scroll"
                        width="50rem"
                    >
                        <Table variant="striped" colorScheme="teal">
                            <TableCaption>Imperial to metric conversion factors</TableCaption>
                            <Thead>
                                <Tr>
                                    <Th textAlign="left">Sentiment</Th>
                                    <Th isNumeric={true}>Score</Th>
                                    <Th textAlign="center">Output</Th>
                                </Tr>
                            </Thead>
                            <Tbody>
                                {sentimentAnalysesBySlug.sentimentAnalyses.map((sentimentAnalysis, index) => {
                                    return (
                                        <Tr key={`sa-tr-${index}`}>
                                            <Td textAlign="left">{sentimentAnalysis.sentiment}</Td>
                                            <Td isNumeric={true}>{sentimentAnalysis.score}</Td>
                                            <Td textAlign="center">
                                                <pre>
                                                    <code>{JSON.stringify(sentimentAnalysis.output)}</code>
                                                </pre>
                                            </Td>
                                        </Tr>
                                    );
                                })}
                            </Tbody>
                            <Tfoot>
                                <Tr>
                                    <Th textAlign="left">Sentiment</Th>
                                    <Th isNumeric={true}>Score</Th>
                                    <Th textAlign="center">Output</Th>
                                </Tr>
                            </Tfoot>
                        </Table>
                    </TableContainer>
                </Flex>
            ) : (
                <NoDataMessage />
            )}
        </Flex>
    );
}

export default SentimentAnalysesBySlugExplorer;

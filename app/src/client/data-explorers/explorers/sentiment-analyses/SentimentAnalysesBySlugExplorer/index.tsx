import React, { useContext, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Flex, Table, Thead, Tbody, Tfoot, Tr, Th, Td, TableCaption, TableContainer } from '@chakra-ui/react';

import { DataExplorersStore } from '@nlpssa-app-types/common/main';
import { NoDataMessage } from 'client/common/components';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { fetchSentimentAnalysesByStockSlug } from 'client/data-explorers/store/actions';

function SentimentAnalysesBySlugExplorer() {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);
    const params = useParams();

    const { sentimentAnalysesBySlug } = state as DataExplorersStore;

    useEffect(() => {
        if (sentimentAnalysesBySlug == null) {
            fetchSentimentAnalysesByStockSlug({ dispatch, stockSlug: params.stockSlug });
        }
    }, [params.stockSlug]);

    console.log('data-explorers.sentiment-analyses - SentimentAnalysesBySlugExplorer', { state });
    return (
        <Flex minWidth="80%">
            {sentimentAnalysesBySlug != null ? (
                <TableContainer
                    className="sentiment-analyses-wrapper"
                    // alignSelf="stretch" flexDirection="column"
                    width="100%"
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
            ) : (
                <NoDataMessage />
            )}
        </Flex>
    );
}

export default SentimentAnalysesBySlugExplorer;

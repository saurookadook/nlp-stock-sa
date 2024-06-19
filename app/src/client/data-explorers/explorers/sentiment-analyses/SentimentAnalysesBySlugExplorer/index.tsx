import React, { useContext, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Flex } from '@chakra-ui/react';

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
        <Flex className="sentiment-analyses-wrapper" alignSelf="stretch" flexDirection="column">
            {sentimentAnalysesBySlug != null ? (
                sentimentAnalysesBySlug.sentimentAnalyses.map((sentimentAnalysis, i) => {
                    return (
                        <Box key={`sa-for-${params.stockSlug}-${i}`}>
                            <p>
                                <b>Sentiment</b>: {sentimentAnalysis.sentiment}
                            </p>
                            <p>
                                <b>Score</b>: {sentimentAnalysis.score}
                            </p>
                            <p>
                                <b>Output:</b>
                            </p>
                            <pre>
                                <code>{JSON.stringify(sentimentAnalysis.output, null, 4)}</code>
                            </pre>
                        </Box>
                    );
                })
            ) : (
                <NoDataMessage />
            )}
        </Flex>
    );
}

export default SentimentAnalysesBySlugExplorer;

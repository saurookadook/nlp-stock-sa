import React, { useContext, useEffect } from 'react';
import { Flex, Heading, SimpleGrid, Text } from '@chakra-ui/react';

import { type DataExplorersStore } from '@nlpssa-app-types/common/main';
import { ButtonLink } from 'client/common/components';
import { baseDataExplorerPath } from 'client/common/constants';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { fetchAllStockData } from 'client/data-explorers/store/stocks/actions';
import { ExplorersList_Flex, ExplorersByStockWrapper_div } from './styled';

function ExplorersList() {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);

    const { stockDataAll } = state as DataExplorersStore;

    useEffect(() => {
        if (stockDataAll == null) {
            fetchAllStockData({ dispatch });
        }
    }, []);

    return (
        <ExplorersList_Flex id="data-explorers-list-wrapper" marginX="auto" maxWidth="60vw">
            <Heading as="h3">General Data Explorers</Heading>
            <SimpleGrid columns={2} spacing={10}>
                <ButtonLink to={`${baseDataExplorerPath}/stocks`}>Stocks</ButtonLink>
                <ButtonLink to={`${baseDataExplorerPath}/article-data`}>Article Data</ButtonLink>
            </SimpleGrid>
            {stockDataAll != null && stockDataAll.length > 0 && (
                <ExplorersList_Flex>
                    <Heading as="h3" textAlign="center">
                        Data Explorers by Stock
                    </Heading>
                    <ExplorersByStockWrapper_div>
                        {stockDataAll.map((stockData, i) => {
                            return (
                                <Flex
                                    key={`stock-explorer-item-${i}`}
                                    alignItems="flex-start"
                                    display="inline-flex"
                                    flexDirection="column"
                                >
                                    <Heading as="h4" fontSize="1.5rem">
                                        {stockData.quoteStockSymbol}
                                    </Heading>
                                    <Text as="span">{stockData.fullStockSymbol}</Text>
                                    <ButtonLink
                                        to={`${baseDataExplorerPath}/sentiment-analyses/${stockData.quoteStockSymbol}`}
                                    >
                                        Sentiment Analysis Explorer
                                    </ButtonLink>
                                    <ButtonLink
                                        to={`${baseDataExplorerPath}/article-data/${stockData.quoteStockSymbol}`}
                                    >
                                        Article Data Explorer
                                    </ButtonLink>
                                    <ButtonLink to={`${baseDataExplorerPath}/stocks/${stockData.quoteStockSymbol}`}>
                                        Stock Explorer
                                    </ButtonLink>
                                </Flex>
                            );
                        })}
                    </ExplorersByStockWrapper_div>
                </ExplorersList_Flex>
            )}
        </ExplorersList_Flex>
    );
}

export default ExplorersList;

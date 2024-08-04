import React, { useContext, useEffect } from 'react';
import { Link as RouterDomLink } from 'react-router-dom';
import { Flex, Heading } from '@chakra-ui/react';

import { type DataExplorersStore } from '@nlpssa-app-types/common/main';
import { baseDataExplorerPath } from 'client/common/constants';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { fetchAllStockData } from 'client/data-explorers/store/stocks/actions';

function ExplorersList() {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);

    const { stockDataAll } = state as DataExplorersStore;

    useEffect(() => {
        if (state.pageData == null) {
            fetchAllStockData({ dispatch });
        }
    }, []);

    return (
        <Flex id="data-explorers-list-wrapper" alignSelf="stretch" flexDirection="column">
            <RouterDomLink to={`${baseDataExplorerPath}/stocks`}>Stocks</RouterDomLink>
            <RouterDomLink to={`${baseDataExplorerPath}/article-data`}>Article Data</RouterDomLink>
            {stockDataAll != null && stockDataAll.length > 0 && (
                <Flex alignSelf="stretch" flexDirection="column">
                    <Heading as="h3" textAlign="center">
                        Sentiment Analysis Data Explorers
                    </Heading>
                    {stockDataAll.map((stockData, i) => {
                        return (
                            <RouterDomLink
                                key={`sa-explorer-link-${i}`}
                                to={`${baseDataExplorerPath}/sentiment-analyses/${stockData.quoteStockSymbol}`}
                            >
                                {stockData.quoteStockSymbol}: {stockData.fullStockSymbol}
                            </RouterDomLink>
                        );
                    })}
                </Flex>
            )}
        </Flex>
    );
}

export default ExplorersList;

import React, { useContext, useEffect } from 'react';
import { Flex } from '@chakra-ui/react';

import { type DataExplorersStore } from '@nlpssa-app-types/common/main';
import { NoDataMessage } from 'client/common/components';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { fetchAllStockData } from 'client/data-explorers/store/stocks/actions';

function AllStocksExplorer() {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);

    const { stockDataAll } = state as DataExplorersStore;

    useEffect(() => {
        if (stockDataAll == null) {
            fetchAllStockData({ dispatch });
        }
    }, []);

    console.log('data-explorers.stocks - AllStocksExplorer', { state, stockDataAll });
    return (
        <Flex className="all-stocks-list-wrapper" alignSelf="stretch" flexDirection="column">
            {stockDataAll != null && stockDataAll.length > 0 ? (
                stockDataAll.map((stockData, i) => {
                    return <pre key={`stock-li-${i}`}>{JSON.stringify(stockData, null, 4)}</pre>;
                })
            ) : (
                <NoDataMessage />
            )}
        </Flex>
    );
}

export default AllStocksExplorer;

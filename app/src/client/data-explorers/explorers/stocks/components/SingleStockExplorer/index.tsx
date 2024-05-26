import React, { useContext, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Flex } from '@chakra-ui/react';

import { DataExplorersStore } from '@nlpssa-app-types/common/main';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { fetchSingularStockData } from 'client/data-explorers/store/stocks/actions';

function SingleStockExplorer() {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);
    const params = useParams();

    const { stockDataSingular } = state as DataExplorersStore;

    useEffect(() => {
        if (stockDataSingular == null) {
            fetchSingularStockData({ dispatch, stockSlug: params.stockSlug });
        }
    }, [params.stockSlug]);

    console.log('data-explorers.stocks - SingleStockExplorer', { state });
    return (
        <Flex className="single-stock-wrapper" alignSelf="stretch" flexDirection="column">
            {stockDataSingular != null ? <pre>{JSON.stringify(stockDataSingular, null, 4)}</pre> : 'No data :['}
        </Flex>
    );
}

export default SingleStockExplorer;

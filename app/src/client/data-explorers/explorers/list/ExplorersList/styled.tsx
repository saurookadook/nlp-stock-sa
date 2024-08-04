import styled from '@emotion/styled';
import { Card, Flex } from '@chakra-ui/react';

const ExplorersList_Flex = styled(Flex)`
    align-items: center;
    flex-direction: column;
    row-gap: 2rem;
`;

const ExplorersByStockWrapper_div = styled.div`
    columns: 15rem auto;
`;

const ExplorersByStockItem_Card = styled(Card)`
    display: inline-flex;
    /* TODO: better way to space out plain CSS columns? */
    margin-bottom: 1rem;
    width: 100%;

    * + * {
        margin-top: 0.5rem;
    }
`;

export { ExplorersList_Flex, ExplorersByStockWrapper_div, ExplorersByStockItem_Card };

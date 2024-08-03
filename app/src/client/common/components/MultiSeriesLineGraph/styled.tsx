import styled from '@emotion/styled';
import { Flex } from '@chakra-ui/react';

const StyledGraphWrapper = styled(Flex)`
    flex-direction: row;
`;

const StyledSVG = styled.svg`
    font: 10px sans-serif;
    height: auto;
    max-width: 100%;
    overflow: visible;
`;

export { StyledGraphWrapper, StyledSVG };

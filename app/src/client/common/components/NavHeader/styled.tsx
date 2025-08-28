import styled from '@emotion/styled';
import { Flex, Link } from '@chakra-ui/react';

const NavHeader_nav = styled.nav`
    border-bottom: 1px solid var(--chakra-colors-gray-400);
    /* border-radius: 5px; */
    padding: 1rem 5rem;
`;

const NavHeader_Flex = styled(Flex)`
    align-items: center;
    column-gap: 1rem;
    flex-direction: row;
`;

const HomeLink_a = styled(Link)`
    &:hover {
        text-decoration: none;
    }
`;

export { NavHeader_nav, NavHeader_Flex, HomeLink_a };

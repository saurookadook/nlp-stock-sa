import styled from '@emotion/styled';
import { Link } from '@chakra-ui/react';

const NavHeader_nav = styled.nav`
    border-bottom: 1px solid var(--chakra-colors-gray-400);
    /* border-radius: 5px; */
    padding: 1rem 5rem;
`;

const HomeLink_a = styled(Link)`
    &:hover {
        text-decoration: none;
    }
`;

export { NavHeader_nav, HomeLink_a };

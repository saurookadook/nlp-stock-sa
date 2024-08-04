import styled from '@emotion/styled';
import { Link as RouterDomLink } from 'react-router-dom';
// import { Link } from '@chakra-ui/react';

const ButtonLink_a = styled(RouterDomLink)`
    border: 1px solid var(--chakra-colors-teal-500);
    border-radius: 5px;
    padding: 0.5rem 1rem;
`;

export { ButtonLink_a };

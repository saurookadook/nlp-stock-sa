import React from 'react';
import { Flex, Heading } from '@chakra-ui/react';

import { NavHeader_nav } from './styled';

function NavHeader({ ...props }) {
    return (
        <NavHeader_nav>
            <Flex alignItems="center" flexDirection="row" {...props}>
                <Heading>{`💸 🤑 💸 Welcome to NLP SSA 💸 🤑 💸`}</Heading>
                {props.children}
            </Flex>
        </NavHeader_nav>
    );
}

export default NavHeader;

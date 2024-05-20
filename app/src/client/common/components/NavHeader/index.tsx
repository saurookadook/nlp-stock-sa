import React from 'react';
import { Flex, Heading } from '@chakra-ui/react';

import { NavHeader_nav, HomeLink_a } from './styled';

function NavHeader({ ...props }) {
    return (
        <NavHeader_nav>
            <Flex alignItems="center" flexDirection="row" {...props}>
                <HomeLink_a href="/app">
                    <Heading>{`💸 🤑 💸 Welcome to NLP SSA 💸 🤑 💸`}</Heading>
                </HomeLink_a>
                {props.children}
            </Flex>
        </NavHeader_nav>
    );
}

export default NavHeader;

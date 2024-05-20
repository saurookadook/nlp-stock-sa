import React from 'react';
import { Flex, Heading, Link } from '@chakra-ui/react';

import { NavHeader_nav } from './styled';

function NavHeader({ ...props }) {
    return (
        <NavHeader_nav>
            <Flex alignItems="center" flexDirection="row" {...props}>
                <Link href="/app">
                    <Heading>{`💸 🤑 💸 Welcome to NLP SSA 💸 🤑 💸`}</Heading>
                </Link>
                {props.children}
            </Flex>
        </NavHeader_nav>
    );
}

export default NavHeader;

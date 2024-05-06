import React from 'react';
import { Flex, Heading } from '@chakra-ui/react';

function NavHeader({ ...props }) {
    return (
        <nav>
            <Flex alignItems="center" flexDirection="row" {...props}>
                <Heading>{`💸 🤑 💸 Welcome to NLP SSA 💸 🤑 💸`}</Heading>
                {props.children}
            </Flex>
        </nav>
    );
}

export default NavHeader;

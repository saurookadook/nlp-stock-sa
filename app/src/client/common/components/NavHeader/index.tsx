import React from 'react';
import { Button, Flex, Heading, useDisclosure } from '@chakra-ui/react';
import { HamburgerIcon } from '@chakra-ui/icons';

import { MainNav } from 'client/common/components';
import { NavHeader_nav, HomeLink_a } from './styled';

function NavHeader({ ...props }) {
    const { isOpen, onOpen, onClose } = useDisclosure();

    return (
        <NavHeader_nav>
            <Flex alignItems="center" flexDirection="row" {...props}>
                <Button // force formatting
                    aria-label="Main navigation button"
                    colorScheme="teal"
                    marginRight="1rem"
                    onClick={onOpen}
                >
                    <HamburgerIcon />
                </Button>
                <MainNav isOpen={isOpen} onClose={onClose} />
                <HomeLink_a href="/app">
                    <Heading>{`💸 Welcome to NLP SSA 💸`}</Heading>
                </HomeLink_a>
                {props.children}
            </Flex>
        </NavHeader_nav>
    );
}

export default NavHeader;

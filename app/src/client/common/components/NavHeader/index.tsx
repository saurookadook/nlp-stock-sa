import React from 'react';
import { Button, Heading, useDisclosure } from '@chakra-ui/react';
import { HamburgerIcon } from '@chakra-ui/icons';

import { MainNav } from 'client/common/components';
import { NavHeader_nav, NavHeader_Flex, HomeLink_a } from './styled';

function NavHeader({ ...props }) {
    const { isOpen, onOpen, onClose } = useDisclosure();

    return (
        <NavHeader_nav>
            <NavHeader_Flex {...props}>
                <Button // force formatting
                    aria-label="Main navigation button"
                    colorScheme="teal"
                    onClick={onOpen}
                >
                    <HamburgerIcon />
                </Button>

                <MainNav isOpen={isOpen} onClose={onClose} />

                <HomeLink_a href="/app">
                    <Heading>{`💸 Welcome to NLP SSA 💸`}</Heading>
                </HomeLink_a>

                {props.children}
            </NavHeader_Flex>
        </NavHeader_nav>
    );
}

export default NavHeader;

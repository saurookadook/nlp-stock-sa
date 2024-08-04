import React from 'react';
import {
    Box,
    Drawer,
    DrawerBody,
    DrawerHeader,
    DrawerOverlay,
    DrawerContent,
    DrawerCloseButton,
    Link,
} from '@chakra-ui/react';

import { basePathPrefix } from 'client/common/constants';

function MainNav({ isOpen, onClose }) {
    return (
        <Drawer placement="top" size="xl" isOpen={isOpen} onClose={onClose}>
            <DrawerOverlay />
            <DrawerContent>
                <DrawerCloseButton />
                <DrawerHeader>{`💸 🤑 💸 Main Navigation 💸 🤑 💸`}</DrawerHeader>
                <DrawerBody paddingTop="var(--chakra-space-4)" paddingBottom="var(--chakra-space-6)">
                    {/* better component to use here? */}
                    <Box as="nav" display="flex" flexDirection="column">
                        <Link href={basePathPrefix}>Home</Link>
                        <Link href={`${basePathPrefix}/data-explorers`}>Data Explorers</Link>
                        <Link href={`${basePathPrefix}/data-explorers/stocks`}>Stocks</Link>
                        <Link href={`${basePathPrefix}/data-explorers/article-data`}>Article Data</Link>
                    </Box>
                    {/* TODO: add links for other pages :] */}
                </DrawerBody>
            </DrawerContent>
        </Drawer>
    );
}

export default MainNav;

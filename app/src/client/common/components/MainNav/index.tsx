import React from 'react';
import {
    Drawer,
    DrawerBody,
    DrawerHeader,
    DrawerOverlay,
    DrawerContent,
    DrawerCloseButton,
    Link,
} from '@chakra-ui/react';

// TODO: move this to `constants` shared between `client` and `server`
const basePathPrefix = '/app';

function MainNav({ isOpen, onClose }) {
    return (
        <Drawer placement="top" size="xl" isOpen={isOpen} onClose={onClose}>
            <DrawerOverlay />
            <DrawerContent>
                <DrawerCloseButton />
                <DrawerHeader>{`💸 🤑 💸 Main Navigation 💸 🤑 💸`}</DrawerHeader>
                <DrawerBody paddingTop="var(--chakra-space-4)" paddingBottom="var(--chakra-space-6)">
                    <nav>
                        <Link href={basePathPrefix}>Home</Link>
                    </nav>
                    <nav>
                        <Link href={`${basePathPrefix}/data-explorers`}>Data Explorers</Link>
                    </nav>
                    <nav>
                        <Link href={`${basePathPrefix}/data-explorers/stocks`}>Stocks</Link>
                    </nav>
                    <nav>
                        <Link href={`${basePathPrefix}/data-explorers/article-data`}>Article Data</Link>
                    </nav>
                    {/* TODO: add links for other pages :] */}
                </DrawerBody>
            </DrawerContent>
        </Drawer>
    );
}

export default MainNav;

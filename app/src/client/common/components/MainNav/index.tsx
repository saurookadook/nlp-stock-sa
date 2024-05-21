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
                        <Link href={`${basePathPrefix}/stocks`}>Stocks</Link>
                    </nav>
                    <nav>
                        <Link href={`${basePathPrefix}/article-data-explorer`}>Article Data Explorer</Link>
                    </nav>
                    {/* TODO: add links for other pages :] */}
                </DrawerBody>
            </DrawerContent>
        </Drawer>
    );
}

export default MainNav;

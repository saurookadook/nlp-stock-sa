import React from 'react';
import { Box, LinkBox, LinkOverlay } from '@chakra-ui/react';

import { GitHubOctocat } from 'client/common/icons';

function GoogleLinkBox({ href }) {
    return (
        <LinkBox
            as="button"
            backgroundColor="blackAlpha.800"
            borderRadius="5px"
            color="white"
            columnGap="0.5rem"
            display="flex"
            paddingY="1rem"
            paddingX="2rem"
        >
            <LinkOverlay href={href} fontWeight="600">{`Log in with GitHub`}</LinkOverlay>
            <Box as="span" display="inline-block" height="1.5rem" width="1.5rem">
                <GitHubOctocat fillColor="#ffffff" />
            </Box>
        </LinkBox>
    );
}

export default GoogleLinkBox;

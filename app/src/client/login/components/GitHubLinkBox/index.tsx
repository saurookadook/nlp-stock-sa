import React from 'react';
import { Box, LinkBox, LinkOverlay } from '@chakra-ui/react';

import { GitHubOctocat } from 'client/common/icons';

function GoogleLinkBox({ href, ...props }) {
    return (
        <LinkBox backgroundColor="blackAlpha.800" color="white" {...props}>
            <LinkOverlay href={href} fontWeight="600">{`Log in with GitHub`}</LinkOverlay>
            <Box as="span" display="inline-block" height="1.5rem" width="1.5rem">
                <GitHubOctocat fillColor="#ffffff" />
            </Box>
        </LinkBox>
    );
}

export default GoogleLinkBox;

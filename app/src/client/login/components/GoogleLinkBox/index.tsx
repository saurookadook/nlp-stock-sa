import React from 'react';
import { Box, LinkBox, LinkOverlay } from '@chakra-ui/react';

function GoogleLinkBox({ href, ...props }) {
    return (
        <LinkBox backgroundColor="#3367d6" color="#ffffff" {...props}>
            <LinkOverlay href={href} fontWeight="600">{`Log in with Google`}</LinkOverlay>
            <Box as="span" display="inline-block" height="1.5rem" width="1.5rem">
                🚧
                {/* <GitHubOctocat fillColor="#ffffff" /> */}
            </Box>
        </LinkBox>
    );
}

export default GoogleLinkBox;

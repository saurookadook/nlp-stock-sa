import React from 'react';
import { Box, LinkBox, LinkOverlay } from '@chakra-ui/react';

function MicrosoftLinkBox({ href, ...props }) {
    return (
        <LinkBox backgroundColor="#fbeaa8" color="#000000" {...props}>
            <LinkOverlay href={href} fontWeight="600">{`Log in with Microsoft`}</LinkOverlay>
            <Box as="span" display="inline-block" height="1.5rem" width="1.5rem">
                🚧
                {/* <GitHubOctocat fillColor="#ffffff" /> */}
            </Box>
        </LinkBox>
    );
}

export default MicrosoftLinkBox;

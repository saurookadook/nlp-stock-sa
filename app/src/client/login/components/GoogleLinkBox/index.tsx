import React from 'react';
import { Box, LinkBox, LinkOverlay } from '@chakra-ui/react';

function GoogleLinkBox({ href }) {
    return (
        <LinkBox
            as="button"
            backgroundColor="#3367d6"
            borderColor="gray.500"
            borderRadius="5px"
            color="#ffffff"
            columnGap="0.5rem"
            display="flex"
            paddingY="1rem"
            paddingX="2rem"
        >
            <LinkOverlay href={href} fontWeight="600">{`Log in with Google`}</LinkOverlay>
            <Box as="span" display="inline-block" height="1.5rem" width="1.5rem">
                🚧
                {/* <GitHubOctocat fillColor="#ffffff" /> */}
            </Box>
        </LinkBox>
    );
}

export default GoogleLinkBox;

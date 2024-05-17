import React from 'react';
import { Box, LinkBox, LinkOverlay } from '@chakra-ui/react';

function AppleLinkBox({ href }) {
    return (
        <LinkBox
            as="button"
            backgroundColor="#ffffff"
            borderColor="gray.500"
            borderRadius="5px"
            color="#000000"
            columnGap="0.5rem"
            display="flex"
            paddingY="1rem"
            paddingX="2rem"
        >
            <LinkOverlay href={href} fontWeight="600">{`Log in with Apple`}</LinkOverlay>
            <Box as="span" display="inline-block" height="1.5rem" width="1.5rem">
                🚧
                {/* <GitHubOctocat fillColor="#ffffff" /> */}
            </Box>
        </LinkBox>
    );
}

export default AppleLinkBox;

import React from 'react';
import { Box, LinkBox, LinkOverlay } from '@chakra-ui/react';

function AppleLinkBox({ href, ...props }) {
    return (
        <LinkBox
            as="div"
            backgroundColor="#ffffff"
            borderColor="gray.500"
            borderStyle="solid"
            borderWidth="1px"
            color="#000000"
            {...props}
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

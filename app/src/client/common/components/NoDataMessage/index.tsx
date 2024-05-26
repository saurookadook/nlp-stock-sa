import React from 'react';
import { Heading, Text, VStack } from '@chakra-ui/react';

function NoDataMessage() {
    return (
        <VStack>
            <Heading display="flex" flexDirection="column">
                <span>💩</span>
                <span>Uh oh...</span>
            </Heading>
            <Text>No data 🥲</Text>
        </VStack>
    );
}

export default NoDataMessage;

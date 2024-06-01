import React from 'react';
import { useRouteError } from 'react-router-dom';
import { Heading, Text, VStack } from '@chakra-ui/react';

type RouterError = {
    message?: string;
    statusText?: string;
};

function ErrorElement() {
    const error = useRouteError() as RouterError;
    console.error(error);

    return (
        <VStack id="error-element">
            {/* TODO: add funny error icon :] */}
            <Heading as="h1">Oops!</Heading>
            <Text>Sorry, an unexpected error has occurred.</Text>
            <Text>
                <i>{error.statusText || error.message}</i>
            </Text>
        </VStack>
    );
}

export default ErrorElement;

import React from 'react';
import { Link as RouterDomLink, type LinkProps } from 'react-router-dom';
import { chakra, useStyleConfig } from '@chakra-ui/react';

const ButtonLink_a = chakra(RouterDomLink);

function ButtonLink({ ...props }: React.PropsWithChildren<LinkProps>) {
    const buttonStyles = useStyleConfig('Button', { colorScheme: 'teal' });

    return (
        <ButtonLink_a
            __css={buttonStyles}
            border="1px solid var(--chakra-colors-teal-500)"
            borderRadius="5px"
            height="auto"
            padding="0.5rem 1rem"
            textAlign="center"
            {...props}
        >
            {props.children}
        </ButtonLink_a>
    );
}

export default ButtonLink;

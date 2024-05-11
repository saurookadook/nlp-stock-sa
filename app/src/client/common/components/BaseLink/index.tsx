import React from 'react';
import { Link } from '@chakra-ui/react';

function BaseLink({ ...props }) {
    return (
        <Link color="teal" {...props}>
            {props.children}
        </Link>
    );
}

export default BaseLink;

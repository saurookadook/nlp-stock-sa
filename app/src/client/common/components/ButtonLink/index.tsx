import React from 'react';
import { type LinkProps } from 'react-router-dom';

import { ButtonLink_a } from 'client/common/components/ButtonLink/styled';

function ButtonLink({ ...props }: React.PropsWithChildren<LinkProps>) {
    return <ButtonLink_a {...props}>{props.children}</ButtonLink_a>;
}

export default ButtonLink;

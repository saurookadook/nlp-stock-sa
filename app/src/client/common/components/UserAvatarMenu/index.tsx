import React from 'react';
import { Avatar, Menu, MenuButton, MenuItem, MenuList } from '@chakra-ui/react';

function UserAvatarMenu({
    username, // force formatting
}: {
    username?: string;
}) {
    function handleOnLogoutClick(e: React.MouseEvent<HTMLButtonElement>) {
        // TODO
    }

    return (
        <Menu>
            <MenuButton>
                <Avatar size="sm" name={username} />
            </MenuButton>

            <MenuList>
                <MenuItem as="a" href="#">
                    Your Profile
                </MenuItem>
                <MenuItem onClick={handleOnLogoutClick}>Logout</MenuItem>
            </MenuList>
        </Menu>
    );
}

export default UserAvatarMenu;

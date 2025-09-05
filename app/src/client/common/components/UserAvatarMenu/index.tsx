import React from 'react';
import { Avatar, Menu, MenuButton, MenuItem, MenuList } from '@chakra-ui/react';

import { AppDispatch } from '@nlpssa-app-types/common/main';
import { attemptLogout } from 'client/common/store/user/actions';

function UserAvatarMenu({
    appDispatch,
    username, // force formatting
}: {
    appDispatch?: AppDispatch;
    username?: string;
}) {
    function handleOnLogoutClick() {
        if (appDispatch == null || typeof appDispatch !== 'function') {
            console.error(
                `[${UserAvatarMenu.name}] Cannot begin logout (hint: Make sure that 'appDispatch' was passed correctly!)`,
            );
            return;
        }

        return attemptLogout({ dispatch: appDispatch }).then((result) => {
            console.log(` [${UserAvatarMenu.name}] logout result `.padStart(90, '-').padEnd(180, '-'));
            console.log({ result });
        });
    }

    return (
        <Menu>
            <MenuButton>
                <Avatar size="sm" name={username} />
            </MenuButton>

            <MenuList>
                {username != null ? (
                    <>
                        <MenuItem as="a" href="/app/account">
                            Your Profile
                        </MenuItem>
                        <MenuItem onClick={handleOnLogoutClick}>Logout</MenuItem>
                    </>
                ) : (
                    <MenuItem as="a" href="/app/login">
                        Login
                    </MenuItem>
                )}
            </MenuList>
        </Menu>
    );
}

export default UserAvatarMenu;

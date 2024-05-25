import * as React from 'react';
import { render } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import { deeplyMerge } from 'client/common/utils';

/**
 * @function renderWithContext
 * @description Utility for rendering stateful components in tests
 */
export const renderWithContext = (
    component: React.ReactElement,
    ProviderRef: any, // TODO: should use React.Provider<any>,
    {
        state = {}, // force formatting
        ...renderOptions
    }: any = {},
) => {
    const baseState = deeplyMerge({}, state);
    return {
        ...render(<ProviderRef initialState={baseState}>{component}</ProviderRef>),
        user: userEvent.setup(),
    };
};

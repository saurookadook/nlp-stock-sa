import React from 'react';
import { screen } from '@testing-library/react';

import { renderWithContext } from 'client/common/utils';
import { HomeApp } from 'client/home/components';
import { AppStateProvider } from 'client/home/store';

describe('home - HomeApp component', () => {
    it('renders correctly', () => {
        renderWithContext(<HomeApp />, AppStateProvider);

        expect(screen.getByText('Welcome to NLP SSA', { exact: false })).toBeVisible();
        expect(screen.getByText('THE MONEY MAKERRRRR', { exact: false })).toBeVisible();
    });
});

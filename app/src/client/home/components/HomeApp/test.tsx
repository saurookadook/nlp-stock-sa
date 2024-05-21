import React from 'react';
import { render, screen } from '@testing-library/react';

import { HomeApp } from 'client/home/components';

describe('home - HomeApp component', () => {
    it('renders correctly', () => {
        render(<HomeApp initialPageData={{ data: [] }} />);

        expect(screen.getByText('Welcome to NLP SSA', { exact: false })).toBeVisible();
        expect(screen.getByText('THE MONEY MAKERRRRR', { exact: false })).toBeVisible();
    });
});

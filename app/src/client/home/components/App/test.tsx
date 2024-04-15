import React from 'react';
import { render, screen } from '@testing-library/react';

import { App } from 'client/home/components';

describe('home - App component', () => {
    it('renders correctly', () => {
        render(<App />);

        expect(screen.getByText("Welcome to NLP SSA", { exact: false })).toBeVisible();
        expect(screen.getByText("THE MONEY MAKERRRRR", { exact: false })).toBeVisible();
    });

})

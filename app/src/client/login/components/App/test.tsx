import React from 'react';
import { render, screen } from '@testing-library/react';

import { App } from 'client/login/components';

describe('login - App component', () => {
    it('renders correctly', () => {
        render(<App />);

        expect(screen.getByText('Login', { exact: false })).toBeVisible();
    });
});

import React from 'react';
import { render, screen } from '@testing-library/react';

import { LoginApp } from 'client/login/components';

describe('login - LoginApp component', () => {
    it('renders correctly', () => {
        render(<LoginApp />);

        expect(screen.getByText('Login', { exact: false })).toBeVisible();
    });
});

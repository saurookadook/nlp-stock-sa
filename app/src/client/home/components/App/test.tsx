import React from 'react';
import { render, screen } from '@testing-library/react';

import { App } from 'client/home/components';

describe('home - App component', () => {
    test('renders learn react link', () => {
        render(<App />);

        expect(screen.getByText("THE MONEY MAKERRRRR", { exact: false })).toBeVisible();
    });

})

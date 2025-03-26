import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import {
    reactRouterOutlets, // force formatting
    reactRouterParameters,
    withRouter,
} from 'storybook-addon-remix-react-router';

import { getStoryStockData } from 'client/_story-data';
import { ExplorersList } from 'client/data-explorers/explorers';
import { dataExplorersRoutes } from 'client/data-explorers/routes';
import { AppStateProvider } from 'client/data-explorers/store';

const meta = {
    title: 'Data Explorers/List/ExplorersList',
    component: ExplorersList,
    decorators: [withRouter],
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
        reactRouter: reactRouterParameters({
            routing: {
                ...reactRouterOutlets(dataExplorersRoutes),
                path: '/data-explorers',
            },
        }),
    },
} satisfies Meta<typeof ExplorersList>;

export default meta;
type Story = StoryObj<typeof meta>;

const stocksData = getStoryStockData().data;

function renderStory() {
    return (
        <AppStateProvider
            initialState={{
                stockDataAll: stocksData,
            }}
        >
            <ExplorersList />
        </AppStateProvider>
    );
}

export const BaseExplorersList: Story = {
    render: renderStory,
};

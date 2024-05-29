import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import {
    reactRouterOutlets, // force formatting
    reactRouterParameters,
    withRouter,
} from 'storybook-addon-remix-react-router';

import type { DataExplorersStore } from '@nlpssa-app-types/common/main';
import { getStoryArticleData } from 'client/_story-data';
import { DataExplorerView } from 'client/data-explorers/layouts';
import { dataExplorersRoutes } from 'client/data-explorers/routes';
import { AppStateProvider } from 'client/data-explorers/store';

const articleData = getStoryArticleData().data as DataExplorersStore['articleData'];

const meta = {
    title: 'Data Explorers/DataExplorerView',
    component: DataExplorerView,
    decorators: [withRouter],
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
        reactRouter: reactRouterParameters({
            routing: reactRouterOutlets(dataExplorersRoutes),
        }),
    },
} satisfies Meta<typeof DataExplorerView>;

export default meta;
type Story = StoryObj<typeof meta>;

const baseInitialData = () => ({
    articleDataBySlug: null,
    articleData: null,
    stockDataAll: null,
    stockDataSingular: null,
});

export const DataExplorerViewArticleData: Story = {
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                path: '/data-explorers/article-data',
            },
        }),
    },
    render: () => {
        return (
            <AppStateProvider
                initialState={{
                    ...baseInitialData(),
                    articleData: articleData,
                }}
            >
                <DataExplorerView />
            </AppStateProvider>
        );
    },
};

export const DataExplorerViewArticleDataNoData: Story = {
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                path: '/data-explorers/article-data',
            },
        }),
    },
    render: () => {
        return (
            <AppStateProvider
                initialState={{
                    ...baseInitialData(),
                    articleData: [],
                }}
            >
                <DataExplorerView />
            </AppStateProvider>
        );
    },
};

export const DataExplorerViewAllStocksNoData: Story = {
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                path: '/data-explorers/stocks',
            },
        }),
    },
    render: () => {
        return (
            <AppStateProvider
                initialState={{
                    ...baseInitialData(),
                    stockDataAll: [],
                }}
            >
                <DataExplorerView />
            </AppStateProvider>
        );
    },
};

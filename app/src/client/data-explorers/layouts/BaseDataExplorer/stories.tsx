import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import {
    reactRouterOutlets, // force formatting
    reactRouterParameters,
    withRouter,
} from 'storybook-addon-remix-react-router';

import type { DataExplorersStore, GenericStateStore } from '@nlpssa-app-types/common/main';
import { getStoryArticleData } from 'client/_story-data';
import { BaseDataExplorer } from 'client/data-explorers/layouts';
import { dataExplorersRoutes } from 'client/data-explorers/routes';

const articleData = getStoryArticleData().data as DataExplorersStore['articleData'];

/**
 * TODO: fix these 🙃
 */
const meta = {
    title: 'Data Explorers/BaseDataExplorer',
    component: BaseDataExplorer,
    decorators: [withRouter],
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
        reactRouter: reactRouterParameters({
            routing: reactRouterOutlets(dataExplorersRoutes),
        }),
    },
} satisfies Meta<typeof BaseDataExplorer>;

export default meta;
type Story = StoryObj<typeof meta>;

const baseInitialData = (): GenericStateStore<DataExplorersStore> => ({
    articleDataBySlug: null,
    articleData: null,
    sentimentAnalysesBySlug: null,
    stockDataAll: null,
    stockDataSingular: null,
});

export const BaseDataExplorerArticleDataNoData: Story = {
    args: {
        initialPageData: {
            ...baseInitialData(),
            articleData: [],
        },
    },
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                path: '/data-explorers/article-data',
            },
        }),
    },
    render: (args) => <BaseDataExplorer initialPageData={args.initialPageData} />,
};

export const BaseDataExplorerArticleData: Story = {
    args: {
        initialPageData: {
            ...baseInitialData(),
            articleData: articleData,
        },
    },
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                path: '/data-explorers/article-data',
            },
        }),
    },
    render: (args) => <BaseDataExplorer initialPageData={args.initialPageData} />,
};

// TODO: is it possible to use controls from Storybook to change the slug value?
export const BaseDataExplorerArticleDataBySlug: Story = {
    args: {
        initialPageData: {
            ...baseInitialData(),
            articleData: articleData,
        },
    },
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                pathParams: { stockSlug: 'DOOG' },
            },
            routing: {
                path: '/data-explorers/article-data/:stockSlug',
            },
        }),
    },
    render: (args) => <BaseDataExplorer initialPageData={args.initialPageData} />,
};

export const BaseDataExplorerStockDataNoData: Story = {
    args: {
        initialPageData: {
            ...baseInitialData(),
            stockDataAll: [],
        },
    },
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                path: '/data-explorers/stocks',
            },
        }),
    },
    render: (args) => {
        return <BaseDataExplorer initialPageData={args.initialPageData} />;
    },
};

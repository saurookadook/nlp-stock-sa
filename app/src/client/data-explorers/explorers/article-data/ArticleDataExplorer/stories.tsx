import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import {
    reactRouterOutlets, // force formatting
    reactRouterParameters,
    withRouter,
} from 'storybook-addon-remix-react-router';

import { InitialArticleDataExplorerPageData } from '@nlpssa-app-types/common/main';
import { getStoryArticleData } from 'client/_story-data';
import { ArticleDataExplorer } from 'client/data-explorers/explorers';
import { dataExplorersRoutes } from 'client/data-explorers/routes';
import { AppStateProvider } from 'client/data-explorers/store';

const meta = {
    title: 'Data Explorers/ArticleData/ArticleDataExplorer',
    component: ArticleDataExplorer,
    decorators: [withRouter],
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
        reactRouter: reactRouterParameters({
            routing: {
                ...reactRouterOutlets(dataExplorersRoutes),
                path: '/data-explorers/article-data',
            },
        }),
    },
} satisfies Meta<typeof ArticleDataExplorer>;

export default meta;
type Story = StoryObj<typeof meta>;

export const BaseArticleDataExplorer: Story = {
    args: getStoryArticleData(),
    render: (args) => {
        const { data } = args as InitialArticleDataExplorerPageData;
        return (
            <AppStateProvider initialState={{ articleData: data }}>
                <ArticleDataExplorer />
            </AppStateProvider>
        );
    },
};

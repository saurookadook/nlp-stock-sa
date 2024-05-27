import React from 'react';
import { createMemoryRouter, RouterProvider } from 'react-router-dom';
import type { Meta, StoryObj } from '@storybook/react';

import type { DataExplorersStore } from '@nlpssa-app-types/common/main';
import storyData from 'client/_story-data';
import { BasePage } from 'client/common/layouts';
import { BaseDataExplorer } from 'client/data-explorers/layouts';
import AppStateProvider from 'client/data-explorers/store/AppStateProvider';
import { dataExplorersRoutes } from 'client/data-explorers/routes';

const meta = {
    title: 'Data Explorers/BaseDataExplorer',
    component: BaseDataExplorer,
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
    },
} satisfies Meta<typeof BaseDataExplorer>;

export default meta;
type Story = StoryObj<typeof meta>;

const baseInitialData = () => ({
    articleDataBySlug: null,
    articleData: null,
    stockDataAll: null,
    stockDataSingular: null,
});

const articleData = storyData.getStoryArticleData().data as DataExplorersStore['articleData'];

export const BaseDataExplorerArticleData: Story = {
    args: {
        initialPageData: {
            ...baseInitialData(),
            articleData: articleData,
        },
    },
    render: (args) => {
        const memoryRouter = createMemoryRouter(dataExplorersRoutes, {
            initialEntries: ['/app/data-explorers/article-data'],
        });

        return (
            <BasePage>
                <AppStateProvider initialState={args.initialPageData}>
                    <RouterProvider router={memoryRouter} />
                </AppStateProvider>
            </BasePage>
        );
    },
};

export const BaseDataExplorerAllStocks: Story = {
    args: {
        initialPageData: {
            ...baseInitialData(),
            articleData: articleData,
        },
    },
    render: (args) => {
        const memoryRouter = createMemoryRouter(dataExplorersRoutes, {
            initialEntries: ['/app/data-explorers/article-data'],
        });

        return (
            <BasePage>
                <AppStateProvider initialState={args.initialPageData}>
                    <RouterProvider router={memoryRouter} />
                </AppStateProvider>
            </BasePage>
        );
    },
};

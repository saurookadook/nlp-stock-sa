import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';

import { InitialArticleDataExplorerPageData } from '@nlpssa-app-types/common/main';
import storyData from 'client/_story-data';
import { ArticleDataExplorer } from 'client/data-explorers/explorers';
import { AppStateProvider } from 'client/data-explorers/store';

const meta = {
    title: 'Data Explorers/ArticleData/ArticleDataExplorer',
    component: ArticleDataExplorer,
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
    },
} satisfies Meta<typeof ArticleDataExplorer>;

export default meta;
type Story = StoryObj<typeof meta>;

export const BaseArticleDataExplorer: Story = {
    args: storyData.getStoryArticleData(),
    render: (args) => {
        const { data } = args as InitialArticleDataExplorerPageData;
        return (
            <AppStateProvider initialState={{ articleData: data }}>
                <ArticleDataExplorer />
            </AppStateProvider>
        );
    },
};

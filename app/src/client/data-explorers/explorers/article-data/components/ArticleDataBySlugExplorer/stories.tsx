import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';

import { InitialArticleDataBySlugPageData } from '@nlpssa-app-types/common/main';
import storyData from 'client/_story-data';
import { ArticleDataBySlugExplorer } from 'client/data-explorers/explorers/article-data/components';
import { AppStateProvider } from 'client/data-explorers/store';

const meta = {
    title: 'Data Explorers/ArticleData/ArticleDataBySlugExplorer',
    component: ArticleDataBySlugExplorer,
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
    },
} satisfies Meta<typeof ArticleDataBySlugExplorer>;

export default meta;
type Story = StoryObj<typeof meta>;

export const BaseArticleDataBySlugExplorer: Story = {
    args: storyData.getStoryArticleDataBySlug(),
    render: (args) => {
        const { data } = args as InitialArticleDataBySlugPageData;
        return (
            <AppStateProvider initialState={{ articleDataBySlug: data }}>
                <ArticleDataBySlugExplorer />
            </AppStateProvider>
        );
    },
};

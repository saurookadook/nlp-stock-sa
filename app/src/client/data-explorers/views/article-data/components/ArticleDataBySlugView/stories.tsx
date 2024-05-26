import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';

import { InitialArticleDataBySlugPageData } from '@nlpssa-app-types/common/main';
import storyData from 'client/_story-data';
import { ArticleDataBySlugView } from 'client/data-explorers/views/article-data/components';
import { AppStateProvider } from 'client/data-explorers/store';

const meta = {
    title: 'Data Explorers/ArticleData/ArticleDataBySlugView',
    component: ArticleDataBySlugView,
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
    },
} satisfies Meta<typeof ArticleDataBySlugView>;

export default meta;
type Story = StoryObj<typeof meta>;

export const BaseArticleDataBySlugView: Story = {
    args: storyData.getStoryArticleDataBySlug(),
    render: (args) => {
        const { data } = args as InitialArticleDataBySlugPageData;
        return (
            <AppStateProvider initialState={{ articleDataBySlug: data }}>
                <ArticleDataBySlugView />
            </AppStateProvider>
        );
    },
};

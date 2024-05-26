import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';

import { InitialArticleDataViewPageData } from '@nlpssa-app-types/common/main';
import storyData from 'client/_story-data';
import { ArticleDataView } from 'client/data-explorers/views/article-data/components';
import { AppStateProvider } from 'client/data-explorers/store';

const meta = {
    title: 'Data Explorers/ArticleData/ArticleDataView',
    component: ArticleDataView,
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
    },
} satisfies Meta<typeof ArticleDataView>;

export default meta;
type Story = StoryObj<typeof meta>;

export const BaseArticleDataView: Story = {
    args: storyData.getStoryArticleData(),
    render: (args) => {
        const { data } = args as InitialArticleDataViewPageData;
        return (
            <AppStateProvider initialState={{ articleData: data }}>
                <ArticleDataView />
            </AppStateProvider>
        );
    },
};

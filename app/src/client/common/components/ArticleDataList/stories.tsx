import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';

import { getStoryArticleData } from 'client/_story-data';
import { ArticleDataList } from 'client/common/components';

const meta = {
    title: 'Common/ArticleDataList',
    component: ArticleDataList,
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
    },
} satisfies Meta<typeof ArticleDataList>;

export default meta;
type Story = StoryObj<typeof meta>;

const { articleData } = getStoryArticleData().data![0];

export const BaseArticleDataList: Story = {
    args: {
        articleData: articleData,
    },
    render: (args) => <ArticleDataList articleData={args.articleData} />,
};

export const BaseArticleDataListNoResults: Story = {
    args: {
        articleData: [],
    },
    render: (args) => <ArticleDataList articleData={args.articleData} />,
};

import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import type { Meta, StoryObj } from '@storybook/react';

import { getStoryPageData } from 'client/_story-data/articleData';
import { ArticleDataList } from 'client/home/components';

const meta = {
    title: 'Home/ArticleDataList',
    component: ArticleDataList,
    decorators: [(story) => <ChakraProvider>{story()}</ChakraProvider>],
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
    },
} satisfies Meta<typeof ArticleDataList>;

export default meta;
type Story = StoryObj<typeof meta>;

const { articleData } = getStoryPageData().data[0];

export const BaseArticleDataList: Story = {
    args: {
        articleData: articleData,
    },
    render: (args) => <ArticleDataList articleData={args.articleData} />,
};

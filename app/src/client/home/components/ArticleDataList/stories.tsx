import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import type { Meta, StoryObj } from '@storybook/react';

import { ArticleDataEntry } from '@nlpssa-app-types/common/main';
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

export const BaseArticleDataList: Story = {
    args: {
        articleData: getStoryPageData().data as ArticleDataEntry[],
    },
    render: (args) => <ArticleDataList articleData={args.articleData} />,
};

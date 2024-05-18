import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import type { Meta, StoryObj } from '@storybook/react';

import { getStoryArticleDataBySlug } from 'client/_story-data/articleDataBySlug';
import { ArticleDataApp } from 'client/article-data/components';
import { AppStateProvider } from 'client/article-data/store';

const meta = {
    title: 'ArticleData/ArticleDataApp',
    component: ArticleDataApp,
    decorators: [(story) => <ChakraProvider>{story()}</ChakraProvider>],
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
    },
} satisfies Meta<typeof ArticleDataApp>;

export default meta;
type Story = StoryObj<typeof meta>;

export const BaseApp: Story = {
    args: getStoryArticleDataBySlug(),
    render: (args) => (
        <AppStateProvider>
            <ArticleDataApp initialPageData={args.initialPageData} stockSlug={args.stockSlug} />
        </AppStateProvider>
    ),
};

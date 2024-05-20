import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';

import { getStoryPageData } from 'client/_story-data/articleData';
import { HomeApp } from 'client/home/components';
import { AppStateProvider } from 'client/home/store';

const meta = {
    title: 'Home/HomeApp',
    component: HomeApp,
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
    },
} satisfies Meta<typeof HomeApp>;

export default meta;
type Story = StoryObj<typeof meta>;

export const BaseApp: Story = {
    args: {
        initialPageData: getStoryPageData(),
    },
    render: (args) => (
        <AppStateProvider>
            <HomeApp initialPageData={args.initialPageData} />
        </AppStateProvider>
    ),
};

import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';

// import { App } from 'client/home/components';
import { getStoryPageData } from 'client/_story-data/articleData';
import { App } from 'client/home/components';
import { AppStateProvider } from 'client/home/store';

// const ProviderDecorator = (story) => <AppStateProvider>{story()}</AppStateProvider>;

const meta = {
    title: 'Home/App',
    component: App,
    // decorators: [ProviderDecorator],
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
    },
} satisfies Meta<typeof App>;

export default meta;
type Story = StoryObj<typeof meta>;

// const storyPageData = getStoryPageData();

export const BaseApp: Story = {
    args: {
        initialPageData: getStoryPageData(),
    },
    render: (args) => (
        <AppStateProvider>
            <App initialPageData={args.initialPageData} />
        </AppStateProvider>
    ),
};

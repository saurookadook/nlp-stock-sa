import React from 'react';
import { useParams } from 'react-router-dom';
import type { Meta, StoryObj } from '@storybook/react';
import {
    reactRouterOutlets, // force formatting
    reactRouterParameters,
    withRouter,
} from 'storybook-addon-remix-react-router';

import { getSentimentAnalysesDataBySlug } from 'client/_story-data';
import { SentimentAnalysesBySlugExplorer } from 'client/data-explorers/explorers';
import { dataExplorersRoutes } from 'client/data-explorers/routes';
import { AppStateProvider } from 'client/data-explorers/store';

const meta = {
    title: 'Data Explorers/SentimentAnalyses/SentimentAnalysesBySlugExplorer',
    component: SentimentAnalysesBySlugExplorer,
    decorators: [withRouter],
    parameters: {
        // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
        layout: 'fullscreen',
        reactRouter: reactRouterParameters({
            routing: {
                ...reactRouterOutlets(dataExplorersRoutes),
                path: '/data-explorers/article-data/:stockSlug',
            },
        }),
    },
} satisfies Meta<typeof SentimentAnalysesBySlugExplorer>;

export default meta;
type Story = StoryObj<typeof meta>;

const sentimentAnalysesDataBySlug = getSentimentAnalysesDataBySlug();

function renderStory() {
    const params = useParams();
    console.log({ params });
    const dataBySlug = sentimentAnalysesDataBySlug[params.stockSlug as string];
    return (
        <AppStateProvider initialState={{ sentimentAnalysesBySlug: dataBySlug }}>
            <SentimentAnalysesBySlugExplorer />
        </AppStateProvider>
    );
}

// TODO: is it possible to use controls from Storybook to change the slug value?
export const BaseSentimentAnalysesBySlugExplorerAMD: Story = {
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                pathParams: { stockSlug: 'AMD' },
            },
        }),
    },
    render: renderStory,
};

export const BaseSentimentAnalysesBySlugExplorerINDO: Story = {
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                pathParams: { stockSlug: 'INDO' },
            },
        }),
    },
    render: renderStory,
};

export const BaseSentimentAnalysesBySlugExplorerKOS: Story = {
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                pathParams: { stockSlug: 'KOS' },
            },
        }),
    },
    render: renderStory,
};

export const BaseSentimentAnalysesBySlugExplorerNTDOF: Story = {
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                pathParams: { stockSlug: 'NTDOF' },
            },
        }),
    },
    render: renderStory,
};

export const BaseSentimentAnalysesBySlugExplorerTSLA: Story = {
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                pathParams: { stockSlug: 'TSLA' },
            },
        }),
    },
    render: renderStory,
};

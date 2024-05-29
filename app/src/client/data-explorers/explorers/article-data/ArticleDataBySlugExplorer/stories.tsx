import React from 'react';
import { useParams } from 'react-router-dom';
import type { Meta, StoryObj } from '@storybook/react';
import {
    reactRouterOutlets, // force formatting
    reactRouterParameters,
    withRouter,
} from 'storybook-addon-remix-react-router';

import { getStoryArticleData } from 'client/_story-data';
import { ArticleDataBySlugExplorer } from 'client/data-explorers/explorers';
import { dataExplorersRoutes } from 'client/data-explorers/routes';
import { AppStateProvider } from 'client/data-explorers/store';

const meta = {
    title: 'Data Explorers/ArticleData/ArticleDataBySlugExplorer',
    component: ArticleDataBySlugExplorer,
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
} satisfies Meta<typeof ArticleDataBySlugExplorer>;

export default meta;
type Story = StoryObj<typeof meta>;

const articleData = getStoryArticleData().data;

// TODO: is it possible to use controls from Storybook to change the slug value?
export const BaseArticleDataBySlugExplorerDOOG: Story = {
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                pathParams: { stockSlug: 'DOOG' },
            },
        }),
    },
    render: () => {
        const params = useParams();
        console.log({ params });
        const dataBySlug = articleData!.find((data) => data.quoteStockSymbol === params.stockSlug);
        return (
            <AppStateProvider initialState={{ articleDataBySlug: dataBySlug }}>
                <ArticleDataBySlugExplorer />
            </AppStateProvider>
        );
    },
};

export const BaseArticleDataBySlugExplorerINDO: Story = {
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                pathParams: { stockSlug: 'INDO' },
            },
        }),
    },
    render: () => {
        const params = useParams();
        console.log({ params });
        const dataBySlug = articleData!.find((data) => data.quoteStockSymbol === params.stockSlug);
        return (
            <AppStateProvider initialState={{ articleDataBySlug: dataBySlug }}>
                <ArticleDataBySlugExplorer />
            </AppStateProvider>
        );
    },
};

export const BaseArticleDataBySlugExplorerKOS: Story = {
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                pathParams: { stockSlug: 'KOS' },
            },
        }),
    },
    render: () => {
        const params = useParams();
        console.log({ params });
        const dataBySlug = articleData!.find((data) => data.quoteStockSymbol === params.stockSlug);
        return (
            <AppStateProvider initialState={{ articleDataBySlug: dataBySlug }}>
                <ArticleDataBySlugExplorer />
            </AppStateProvider>
        );
    },
};

export const BaseArticleDataBySlugExplorerNTDOF: Story = {
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                pathParams: { stockSlug: 'NTDOF' },
            },
        }),
    },
    render: () => {
        const params = useParams();
        console.log({ params });
        const dataBySlug = articleData!.find((data) => data.quoteStockSymbol === params.stockSlug);
        return (
            <AppStateProvider initialState={{ articleDataBySlug: dataBySlug }}>
                <ArticleDataBySlugExplorer />
            </AppStateProvider>
        );
    },
};

export const BaseArticleDataBySlugExplorerTSLA: Story = {
    parameters: {
        reactRouter: reactRouterParameters({
            location: {
                pathParams: { stockSlug: 'TSLA' },
            },
        }),
    },
    render: () => {
        const params = useParams();
        console.log({ params });
        const dataBySlug = articleData!.find((data) => data.quoteStockSymbol === params.stockSlug);
        return (
            <AppStateProvider initialState={{ articleDataBySlug: dataBySlug }}>
                <ArticleDataBySlugExplorer />
            </AppStateProvider>
        );
    },
};

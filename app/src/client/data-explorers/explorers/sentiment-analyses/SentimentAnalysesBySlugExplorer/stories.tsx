import React from 'react';
import { useParams } from 'react-router-dom';
import type { Meta, StoryObj } from '@storybook/react';
import {
  reactRouterOutlets, // force formatting
  reactRouterParameters,
  withRouter,
} from 'storybook-addon-remix-react-router';

import { SentimentAnalysesDataEntry } from '@nlpssa-app-types/common/main';
import {
  getStoryArticleData,
  getSentimentAnalysesDataBySlug,
} from 'client/_story-data';
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
        path: '/data-explorers/sentiment-analyses/:stockSlug',
      },
    }),
  },
} satisfies Meta<typeof SentimentAnalysesBySlugExplorer>;

export default meta;
type Story = StoryObj<typeof meta>;

const articleData = getStoryArticleData().data;
const sentimentAnalysesDataBySlug = getSentimentAnalysesDataBySlug();

function dateFieldIsValid(dateField: unknown) {
  return dateField != null && typeof dateField === 'string' && dateField !== '';
}

// TODO: the creation of the date fields here is only temporary; that kind of
// normalization should probably be done in the reducer
const filterNullSourcesAndSortData = (data: SentimentAnalysesDataEntry[]) =>
  data
    .filter((d) => d.source != null)
    .map(function (d) {
      if (dateFieldIsValid(d.source?.data?.last_updated_date)) {
        d.source!.data!.last_updated_date = new Date(
          d.source!.data!.last_updated_date as string,
        );
      }
      if (dateFieldIsValid(d.source?.data?.published_date)) {
        d.source!.data!.published_date = new Date(
          d.source!.data!.published_date as string,
        );
      }
      return d;
    })
    .sort(function (a: SentimentAnalysesDataEntry, b: SentimentAnalysesDataEntry) {
      const aField = a.source!.data!.last_updated_date as Date;
      const bField = b.source!.data!.last_updated_date as Date;

      return aField == bField ? 0 : Number(aField > bField) - Number(aField < bField);
    });

function renderStory() {
  const params = useParams();
  console.log({ params });

  const _articleDataBySlug = articleData!.find(
    (data) => data.quoteStockSymbol === params.stockSlug,
  );
  const _sentimentAnalysesDataBySlug =
    sentimentAnalysesDataBySlug[params.stockSlug as string];

  return (
    <AppStateProvider
      initialState={{
        articleDataBySlug: _articleDataBySlug,
        sentimentAnalysesBySlug: {
          quoteStockSymbol: _sentimentAnalysesDataBySlug.quoteStockSymbol,
          sentimentAnalyses: filterNullSourcesAndSortData(
            _sentimentAnalysesDataBySlug.sentimentAnalyses,
          ),
        },
      }}
    >
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

import React, { useContext, useEffect, useMemo } from 'react';
import { useParams } from 'react-router-dom';
import {
  Heading, // force formatting
  Spinner,
  Table,
  Thead,
  Tbody,
  Tfoot,
  Tr,
  Th,
  Td,
  TableCaption,
  TableContainer,
} from '@chakra-ui/react';

import { DataExplorersStore } from '@nlpssa-app-types/common/main';
import { MultiSeriesLineGraph, NoDataMessage } from 'client/common/components';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { ArticleDataBySlugExplorer } from 'client/data-explorers/explorers';
import { fetchSentimentAnalysesByStockSlug } from 'client/data-explorers/store/actions';
import { StyledFlex, StyledTd } from './styled';

function SentimentAnalysesBySlugExplorer() {
  const state = useContext(BaseStateContext);
  const dispatch = useContext(BaseDispatchContext);
  const params = useParams();

  const { sentimentAnalysesBySlug } = state as DataExplorersStore;

  const scoresColumns = useMemo(() => {
    const { output } = sentimentAnalysesBySlug?.sentimentAnalyses?.[0] || {};
    if (output == null) {
      return [];
    }

    // TODO: maybe this could be a util function and return an array of objects
    // with key and header display value
    const sortedColumns = Object.keys(output).sort((a, b) => {
      if (a === 'compound' || b === 'compound') {
        return 1;
      }

      return a.localeCompare(b) > 0 ? -1 : 1;
    });

    return sortedColumns;
  }, [sentimentAnalysesBySlug]);

  useEffect(() => {
    console.log({
      component: 'SentimentAnalysesBySlugExplorer',
      shouldReloadGraph: shouldReloadGraph(sentimentAnalysesBySlug, params.stockSlug),
    });
    if (shouldReloadGraph(sentimentAnalysesBySlug, params.stockSlug)) {
      fetchSentimentAnalysesByStockSlug({
        dispatch,
        stockSlug: params.stockSlug,
      });
    }
  }, [
    params.stockSlug,
    (state.sentimentAnalysesBySlug as DataExplorersStore['sentimentAnalysesBySlug'])
      ?.sentimentAnalyses,
  ]);

  console.log('data-explorers.sentiment-analyses - SentimentAnalysesBySlugExplorer', {
    scoresColumns,
    state,
  });
  return (
    <StyledFlex alignSelf="start" minWidth="80%" paddingX="4rem" rowGap="2rem">
      <Heading>Sentiment Analysis for {params.stockSlug}</Heading>

      {(sentimentAnalysesBySlug || {}).sentimentAnalyses != null ? (
        <StyledFlex columnGap="2rem" flexDirection="row">
          <StyledFlex
            justifyContent="center" // force formatting
            minHeight="30rem"
          >
            {shouldReloadGraph(sentimentAnalysesBySlug, params.stockSlug) ? (
              <Spinner // force formatting
                color="teal"
                emptyColor="gray.200"
                size="xl"
                speed="0.65s"
                thickness="4px"
              />
            ) : (
              <MultiSeriesLineGraph
                sentimentAnalysesData={sentimentAnalysesBySlug.sentimentAnalyses}
                width={16 * 70}
              />
            )}
          </StyledFlex>

          <TableContainer
            className="sentiment-analyses-wrapper"
            // alignSelf="stretch" flexDirection="column"
            maxHeight="32rem"
            overflowY="scroll"
            width="50rem"
          >
            <Table variant="striped" colorScheme="teal">
              <TableCaption>Imperial to metric conversion factors</TableCaption>

              <Thead>
                <TableHeadersRow />
              </Thead>

              <Tbody>
                {sentimentAnalysesBySlug.sentimentAnalyses.map((sentimentAnalysis) => {
                  return (
                    <Tr
                      key={`sa-tr-${sentimentAnalysis.id}`}
                      data-sa-id={sentimentAnalysis.id}
                    >
                      <Td textAlign="left">{sentimentAnalysis.sentiment}</Td>

                      {Object.keys(sentimentAnalysis.output).map((polarityKey) => {
                        const polarityValue = sentimentAnalysis.output[polarityKey];

                        return (
                          <StyledTd
                            key={polarityKey}
                            data-polarity-key={polarityKey}
                            data-polarity-value={polarityValue}
                            textAlign="left"
                          >
                            <pre>
                              <code>{polarityValue}</code>
                            </pre>
                          </StyledTd>
                        );
                      })}
                    </Tr>
                  );
                })}
              </Tbody>

              <Tfoot>
                <TableHeadersRow />
              </Tfoot>
            </Table>
          </TableContainer>
        </StyledFlex>
      ) : (
        <NoDataMessage />
      )}

      <ArticleDataBySlugExplorer dataListOnly={true} />
    </StyledFlex>
  );
}

function TableHeadersRow() {
  return (
    <Tr>
      <Th textAlign="left">Sentiment</Th>
      <Th textAlign="left">Score</Th>
      <Th textAlign="left">Positive (pos)</Th>
      <Th textAlign="left">Neutral (neu)</Th>
      <Th textAlign="left">Negative (neg)</Th>
    </Tr>
  );
}

function shouldReloadGraph(
  sentimentAnalysesBySlug: DataExplorersStore['sentimentAnalysesBySlug'],
  stockSlugFromParams: string = '',
) {
  return (
    sentimentAnalysesBySlug == null ||
    sentimentAnalysesBySlug.quoteStockSymbol !== stockSlugFromParams
    // (sentimentAnalysesBySlug != null &&
    //   sentimentAnalysesBySlug.quoteStockSymbol !== stockSlugFromParams)
  );
}

export default SentimentAnalysesBySlugExplorer;

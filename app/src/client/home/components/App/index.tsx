import React, { useContext, useEffect } from 'react';
import { Center, Container, Flex } from '@chakra-ui/react';

import { ArticleDataEntry } from '@nlpssa-app-types/common/main';
import { BasePage } from 'client/common/layouts';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store/contexts';
import { ArticleDataList } from 'client/home/components';
import { fetchArticleData } from 'client/home/store/actions';
// import logo from '/logo.svg';

type PageData = Record<string, unknown>[];

interface InitialPageData {
    data: PageData | null;
}

function App({ initialPageData }: { initialPageData: InitialPageData }): React.ReactElement {
    const state = useContext(BaseStateContext);
    const dispatch = useContext(BaseDispatchContext);

    const pageData = initialPageData.data || state.pageData;

    useEffect(() => {
        if (state.pageData == null) {
            fetchArticleData({ dispatch });
        }
    });

    console.log('home - App', { initialPageData, pageData });
    return (
        <BasePage
            pageTitle={
                <span>
                    <b>Home</b>: Article Data
                </span>
            }
        >
            <Container className="home" style={{ margin: '0 auto' }} maxWidth="75vw">
                <Center
                    borderColor="gray.400"
                    borderRadius="5px"
                    borderStyle="solid"
                    borderTopWidth="0px"
                    borderRightWidth="1px"
                    borderBottomWidth="0px"
                    borderLeftWidth="1px"
                    flexDirection="column"
                    // h="50vh"
                    w="100%"
                >
                    <Flex flexDirection="column">
                        {pageData != null && (pageData as PageData).length > 0 ? (
                            <ArticleDataList articleData={pageData as ArticleDataEntry[]} />
                        ) : (
                            'No data :['
                        )}
                    </Flex>
                </Center>
            </Container>
        </BasePage>
    );
}

export default App;

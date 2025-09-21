import React, { useMemo } from 'react';
import { Outlet, useLocation, useParams } from 'react-router-dom';
import { Center, Container } from '@chakra-ui/react';

function DataExplorerView() {
  const location = useLocation();
  const params = useParams();

  console.log({
    location,
    params,
  });

  const dataExplorerViewType = useMemo(() => {
    const dataEntity = (location.pathname.match(
      /(?<=(\/app)?\/data-explorers\/)[^\/]+?(?=\/|$)/gim,
    ) || [])[0];
    const { stockSlug } = params;

    return stockSlug != null // force formatting
      ? `${dataEntity}-by-slug`
      : dataEntity;
  }, [location, params]);

  const containerClassName = useMemo(() => {
    return ['data-explorer-view', dataExplorerViewType].join(' ');
  }, [dataExplorerViewType]);

  return (
    <Container
      className={containerClassName}
      margin="0 auto"
      maxWidth={
        // TODO: this feels dirty lol
        dataExplorerViewType === 'sentiment-analyses-by-slug' ? '100vw' : '75vw'
      }
    >
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
        <Outlet />
      </Center>
    </Container>
  );
}

export default DataExplorerView;

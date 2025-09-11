import React from 'react';
import { Outlet } from 'react-router-dom';
import { Center, Container } from '@chakra-ui/react';

function DataExplorerView() {
  return (
    <Container className="data-explorer-view" margin="0 auto" maxWidth="75vw">
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

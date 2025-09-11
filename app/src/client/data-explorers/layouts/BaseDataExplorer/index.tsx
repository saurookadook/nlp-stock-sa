import React, { useContext } from 'react';
import { RouterProvider } from 'react-router-dom';

import type {
  DataExplorersStore,
  GenericStateStore,
} from '@nlpssa-app-types/common/main';
import { BasePage } from 'client/common/layouts';
import { BaseStateContext, BaseDispatchContext } from 'client/common/store';
import browserRouter from 'client/data-explorers/routes';

function BaseDataExplorer() {
  const state = useContext(BaseStateContext);
  const dispatch = useContext(BaseDispatchContext);

  const { user } = state as GenericStateStore<DataExplorersStore>;

  console.log(`[data-explorers - ${BaseDataExplorer.name}]\n`, { state });

  return (
    <BasePage // force formatting
      appDispatch={dispatch}
      pageTitle={`Data Explorers: <something-dynamic-here>`}
      userData={user}
    >
      <RouterProvider router={browserRouter} />
    </BasePage>
  );
}

export default BaseDataExplorer;

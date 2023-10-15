import React from 'react';
import { RecoilRoot } from 'recoil';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { NAVIGATION_LIST } from "./applications/navigations";

function App() {
  return (
    <RecoilRoot>
      <BrowserRouter>
        <Routes>
          {NAVIGATION_LIST.map(navigation_url => <Route path={navigation_url.url} element={<navigation_url.page />} />)}
        </Routes>
      </BrowserRouter>
    </RecoilRoot>
  );
}

export default App;

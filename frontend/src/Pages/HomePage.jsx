import React from "react";
import { useState } from "react";
import { Layout } from "antd";
import AppHeader from "../Components/Layout/AppHeader";
import AppSider from "../Components/Layout/AppSider";
import AppContent from "../Components/Layout/AppContent";
import { useAuth } from "../AuthContext";
import MainUnauthorizedPage from "../Components/MainUnauthorizedPage";
import CreateTaskTypeForm from "../Components/Forms/CreateTaskTypeForm";
import CreateTestForm from "../Components/Forms/CreateTestForm";

export default function HomePage() {
  const { isAuthenticated } = useAuth();
  const [siderState, setSiderState] = useState(true);
  console.log(isAuthenticated);

  function SiderStateChanged() {
    console.log("clicked");
    setSiderState(!siderState);
  }

  return (
    <Layout>
      <AppHeader onClick={SiderStateChanged} />
      <Layout>
        {isAuthenticated ? <AppSider siderState={siderState} /> : <></>}
        <AppContent>
          {isAuthenticated ? (
            <>
              <CreateTaskTypeForm />
            </>
          ) : (
            <MainUnauthorizedPage />
          )}
        </AppContent>
      </Layout>
    </Layout>
  );
}

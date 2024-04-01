import React, { useEffect, useState } from "react";

import ViewTable from "../Components/Forms/Table";
import { FetchTests } from "../Handlers/API";
import BasePage from "../Components/Layout/BasePage";

export default function AllTestsPage() {
  const [tests, setTests] = useState([]);

  useEffect(() => {
    FetchTests({ setter: setTests });
  }, []);

  return (
    <BasePage>
      <ViewTable type="test" data={tests} />
    </BasePage>
  );
}

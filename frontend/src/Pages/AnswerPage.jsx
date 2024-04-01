import React, { useEffect } from "react";
import { useParams } from "react-router-dom";

import BasePage from "../Components/Layout/BasePage";

export default function AnswerPage() {
  const { id, answer_id } = useParams();
  console.log("From path: ", id, answer_id);

  return (
    <BasePage>
      <div>
        <h2>Test Answer Page</h2>
        <p>Test ID: {id}</p> 
        <p>Answer ID: {answer_id}</p>
      </div>
    </BasePage>
  );
}

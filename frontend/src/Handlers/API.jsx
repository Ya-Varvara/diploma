import React from "react";

export const FetchTests = async ({ setter }) => {
  try {
    const response = await fetch("http://localhost:8000/test/", {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Tests fetching failed: " + response.status);
    }
    const data = await response.json();
    setter(data);
  } catch (error) {
    console.error(error);
  }
};

export const FetchTestByID = async ({ setter, id }) => {
  try {
    const response = await fetch(`http://localhost:8000/test/${id}`, {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Test fetching failed: " + response.status);
    }
    const data = await response.json();
    console.log("In Fetch Test By ID: ", data);
    setter(data);
  } catch (error) {
    console.error(error);
  }
};

// export const FetchTestByLink = async ({ setter, link }) => {
//   try {
//     const response = await fetch(`http://localhost:8000/test/variant/${link}`, {
//       method: "GET",
//     });
//     if (!response.ok) {
//       throw new Error("Test variant fetching failed: " + response.status);
//     }
//     const data = await response.json();
//     console.log("In Fetch Test By Link: ", data);
//     setter(data);
//   } catch (error) {
//     console.error(error);
//   }
// };

export const FetchTestByLink = async ({ link }) => {
  try {
    const response = await fetch(`http://localhost:8000/test/variant/${link}`, {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error("Test variant fetching failed: " + response.status);
    }
    const data = await response.json();
    console.log("In Fetch Test By Link: ", data);
    return data; // Возвращаем данные
  } catch (error) {
    console.error(error);
    throw error; // Пробрасываем ошибку дальше, чтобы обработать её в вызывающем коде
  }
};

export const PostTest = async ({ requestBody }) => {
  try {
    const response = await fetch("http://localhost:8000/test/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(requestBody),
    });
    if (!response.ok) {
      throw new Error("Test creation failed with status: " + response.status);
    }
    console.log("Test was created successfully");
  } catch (error) {
    console.error(error);
  }
};

export const FetchTaskTypes = async ({ setter }) => {
  try {
    const response = await fetch("http://localhost:8000/task_type/", {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Task Types fetching failed: " + response.status);
    }
    const data = await response.json();
    setter(data);
  } catch (error) {
    console.error(error);
  }
};

export const FetchTaskTypeByID = async ({ setter, id }) => {
  try {
    const response = await fetch(`http://localhost:8000/task_type/${id}`, {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Task Type fetching failed: " + response.status);
    }
    const data = await response.json();
    console.log("In Fetch Task Type By ID: ", data);
    setter(data);
  } catch (error) {
    console.error(error);
  }
};

export const PostTaskTypes = async ({ requestBody }) => {
  try {
    const response = await fetch("http://localhost:8000/task_type/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(requestBody),
    });
    if (!response.ok) {
      throw new Error(
        "Task Type creation failed with status: " + response.status
      );
    }
    console.log("Task Type was created successfully");
  } catch (error) {
    console.error(error);
  }
};

export const FetchBaseTaskTypes = async ({ setter }) => {
  try {
    const response = await fetch(
      "http://localhost:8000/task_type/base_types/",
      {
        method: "GET",
        credentials: "include",
      }
    );
    if (!response.ok) {
      throw new Error("Base Task Types fetching failed: " + response.status);
    }
    const data = await response.json();
    setter(data);
  } catch (error) {
    console.error(error);
  }
};

export const FetchForms = async ({ setter }) => {
  try {
    const response = await fetch("http://localhost:8000/forms/", {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Forms fetching failed: " + response.status);
    }
    const data = await response.json();
    setter(data);
  } catch (error) {
    console.error(error);
  }
};

export const PostRegister = async ({ requestBody }) => {
  try {
    const response = await fetch("http://localhost:8000/auth/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(requestBody),
    });
    if (!response.ok) {
      throw new Error("Register failed with status: " + response.status);
    }
    console.log("Register successful!");
  } catch (error) {
    console.error(error);
  }
};

export const PostLogin = async ({ formData }) => {
  try {
    const response = await fetch("http://localhost:8000/auth/login/", {
      method: "POST",
      credentials: "include",
      body: formData,
    });
    if (!response.ok) {
      throw new Error("Login failed with status: " + response.status);
    }
    console.log("Login successful!");
  } catch (error) {
    console.error(error);
  }
};

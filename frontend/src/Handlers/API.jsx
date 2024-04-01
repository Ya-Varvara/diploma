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

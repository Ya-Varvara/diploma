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

export const FetchTestByLink = async ({ link }) => {
  try {
    const response = await fetch(
      `http://localhost:8000/test/variant/${link}/`,
      {
        method: "GET",
      }
    );
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

export const DeleteTestByID = async ({ id }) => {
  try {
    const response = await fetch(`http://localhost:8000/test/${id}/`, {
      method: "DELETE", // Изменение на метод DELETE
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Test deletion failed: " + response.status);
    }
    console.log("Test successfully deleted with ID:", id);
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

export const DeleteTaskTypeByID = async ({ id }) => {
  try {
    const response = await fetch(`http://localhost:8000/task_type/${id}/`, {
      method: "DELETE",
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Task Type deleting failed: " + response.status);
    }
    const data = await response.json();
    console.log("Task Type successfully deleted with ID:", id);
    setter(data);
  } catch (error) {
    console.error(error);
  }
};

export const FetchTaskTypeByID = async ({ id }) => {
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

export const FetchTestTaskResult = async ({ setter, test_id, variant }) => {
  try {
    const queryParams = `test_id=${test_id}&variant=${variant}`; // Создание строки запроса
    const response = await fetch(
      `http://localhost:8000/test_task_result/?${queryParams}`,
      {
        method: "GET",
        credentials: "include",
      }
    );
    if (!response.ok) {
      throw new Error("Test Task Results fetching failed: " + response.status);
    }
    const data = await response.json();
    setter(data);
  } catch (error) {
    console.error(error);
  }
};

export const PostTestTaskResult = async ({ requestBody }) => {
  try {
    const response = await fetch("http://localhost:8000/test_task_result/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    });
    if (!response.ok) {
      throw new Error(
        "Test task result creation failed with status: " + response.status
      );
    }
    console.log("Test task result was created successfully");
  } catch (error) {
    console.error(error);
  }
};

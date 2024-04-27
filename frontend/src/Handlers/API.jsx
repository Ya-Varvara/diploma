export const baseURL = "http://localhost:8000";

export const FetchTests = async ({ setter }) => {
  try {
    const response = await fetch(`${baseURL}/test/`, {
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
    const response = await fetch(`${baseURL}/test/${id}`, {
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

export const DeleteTestByID = async ({ id }) => {
  try {
    const response = await fetch(`${baseURL}/test/${id}/`, {
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
    const response = await fetch(`${baseURL}/test/`, {
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
    const response = await fetch(`${baseURL}/task_type/`, {
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
    const response = await fetch(`${baseURL}/task_type/${id}/`, {
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
    const response = await fetch(`${baseURL}/task_type/${id}`, {
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
    const response = await fetch(`${baseURL}/task_type/`, {
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
    const response = await fetch(`${baseURL}/task_type/base_types/`, {
      method: "GET",
      credentials: "include",
    });
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
    const response = await fetch(`${baseURL}/forms/`, {
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
    const response = await fetch(`${baseURL}/auth/register/`, {
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
    const response = await fetch(`${baseURL}/auth/login/`, {
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

export const FetchVariantsResult = async ({ setter, test_id }) => {
  try {
    const response = await fetch(`${baseURL}/variant/${test_id}/`, {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Test Task Results fetching failed: " + response.status);
    }
    const data = await response.json();
    console.log(data);
    setter(data);
  } catch (error) {
    console.error(error);
  }
};

export const PostVariantResult = async ({ requestBody }) => {
  try {
    const response = await fetch(`${baseURL}/variant/result/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    });
    if (!response.ok) {
      throw new Error(
        "Variant result creation failed with status: " + response.status
      );
    }
    console.log("Test task result was created successfully");
  } catch (error) {
    console.error(error);
  }
};

export const FetchTestVariantByLink = async ({ link }) => {
  try {
    const response = await fetch(`${baseURL}/variant/?link=${link}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
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

export const MakeTestVariantGiven = async ({ id }) => {
  try {
    const response = await fetch(`${baseURL}/variant/make_given/?id=${id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      throw new Error("Test variant making given failed: " + response.status);
    }
  } catch (error) {
    console.error(error);
    throw error; // Пробрасываем ошибку дальше, чтобы обработать её в вызывающем коде
  }
};

export const sendFileToServer = async ({ data, variant_id }) => {
  const url = `${baseURL}/upload/?variant_id=${variant_id}`;
  console.log(data, variant_id);

  try {
    const response = await fetch(url, {
      method: "POST",
      body: data,
    });

    if (!response.ok) {
      throw new Error(
        `Server returned ${response.status}: ${response.statusText}`
      );
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Ошибка при отправке файла:", error);
    throw error;
  }
};

import { getToken } from "./jwtToken";

export function changeProject(data, projectId) {
  let headers = {
    Authorization: "",
    "Content-Type": "application/json",
  };
  const response = getToken().then((token) => {
    headers.Authorization = `Bearer ${token}`;
    try {
      const response = fetch(
        `http://kematin.space:9999/admin/project/${projectId}`,
        {
          method: "PUT",
          headers: headers,
          body: JSON.stringify(data),
        }
      ).then((response) => {
        return response;
      });
      return response;
    } catch (error) {
      console.error("Error updating project:", error);
      throw error;
    }
  });
  return response;
}

export async function changeFiles(projectId, files) {
  const token = await getToken();
  let headers = {
    Authorization: `Bearer ${token}`,
  };

  const apiUrl = `http://kematin.space:9999/admin/files/${projectId}`;
  const data = new FormData();

  if (files.doc_file && files.doc_file !== "HAVE") {
    data.append("doc_file", files.doc_file);
  }
  if (files.cover_file && files.cover_file !== "HAVE") {
    data.append("cover_file", files.cover_file);
  }

  if (files.pptx_file && files.pptx_file !== "HAVE") {
    data.append("pptx_file", files.pptx_file);
  }

  if (files.unique_file && files.unique_file !== "HAVE") {
    console.log("ADD UNIQUE");
    data.append("unique_file", files.unique_file);
  }

  if (files.product_files && files.product_files !== "HAVE") {
    console.log("ADD PRODUCT");
    files.product_files.forEach((productFile) => {
      data.append("product_files", productFile);
    });
  }

  if (
    data.has("doc_file") ||
    data.has("pptx_file") ||
    data.has("cover_file") ||
    data.has("unique_file") ||
    data.has("product_files")
  ) {
    console.log("CHANGE PROJECT FILES");

    try {
      const response = await fetch(apiUrl, {
        method: "PUT",
        body: data,
        headers: headers,
      });

      const responseData = await response.json();
      console.log("Success:", responseData);
      return responseData;
    } catch (error) {
      console.error("Error:", error);
      return error;
    }
  } else {
    return null;
  }
}

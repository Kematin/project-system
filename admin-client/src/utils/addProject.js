import { getToken } from "./jwtToken";

export function addProject(data) {
  let headers = {
    Authorization: "",
    "Content-Type": "application/json",
  };
  const response = getToken().then((token) => {
    headers.Authorization = `Bearer ${token}`;
    const apiUrl = "http://kematin.space:9999/admin/project";
    const response = fetch(apiUrl, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(data),
    });
    return response;
  });
  return response;
}

export function addFiles(projectId, files) {
  let headers = {
    Authorization: "",
  };
  const response = getToken().then((token) => {
    headers.Authorization = `Bearer ${token}`;
    const apiUrl = `http://kematin.space:9999/admin/files/${projectId}`;
    const data = new FormData();

    data.append("doc_file", files.doc_file);
    data.append("cover_file", files.cover_file);
    if (files.pptx_file) {
      data.append("pptx_file", files.pptx_file);
    }
    if (files.unique_file) {
      data.append("unique_file", files.unique_file);
    }

    if (files.product_files) {
      files.product_files.forEach((productFile, index) => {
        data.append(`product_files`, productFile);
      });
    }

    fetch(apiUrl, {
      method: "POST",
      body: data,
      headers: headers,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
  return response;
}

import React, { useState, useEffect } from "react";
import { addProject, addFiles } from "../../utils/addProject";
import { useNavigate } from "react-router-dom";
import { getToken } from "../../utils/jwtToken";
import "./index.css";

function InputField({ label, value, onChange }) {
  return (
    <div>
      <label className="label-text">{label}</label>
      <input
        className="input-field w-full py-3 border border-slate-200 rounded-lg px-3 focus:outline-none focus:border-slate-500 hover:shadow dark:bg-gray-600 dark:text-gray-100"
        value={value}
        onChange={onChange}
        type="text"
      />
    </div>
  );
}

function TextArea({ label, value, onChange }) {
  return (
    <div>
      <label className="label-text">{label}</label>
      <textarea
        value={value}
        onChange={onChange}
        className="w-full py-3 border border-slate-200 rounded-lg px-3 focus:outline-none focus:border-slate-500 hover:shadow dark:bg-gray-600 dark:text-gray-100"
      ></textarea>
    </div>
  );
}

function UploadFile({ name, file, setFile, idSuffix }) {
  const inputId = `upload ${idSuffix}`;
  let handleFileChange = () => {};
  if (inputId === "upload product") {
    handleFileChange = (event) => {
      const files = event.target.files;
      setFile([...file, ...files]);
    };
  } else {
    handleFileChange = (event) => {
      const file = event.target.files[0];
      setFile(file);
    };
  }

  return (
    <div className="rounded-md border-2 border-indigo-500 bg-transparent-50 p-4 shadow-md w-36">
      <label
        htmlFor={inputId}
        className="flex flex-col items-center gap-2 cursor-pointer"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-10 w-10 fill-white stroke-indigo-500"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        {inputId === "upload product" ? (
          <span className="label-text font-medium">
            {file.length != 0 ? "✔️" : name}
          </span>
        ) : (
          <span className="label-text font-medium">{file ? "✔️" : name}</span>
        )}
      </label>
      <input
        id={inputId}
        type="file"
        className="hidden"
        onChange={handleFileChange}
        multiple
      />
    </div>
  );
}

function SelectFromListInput({ label, options, onChange }) {
  const [selectedValue, setSelectedValue] = useState("");

  const handleSelectChange = (event) => {
    const newValue = event.target.value;
    setSelectedValue(newValue);

    onChange(newValue);
  };

  return (
    <div className="mb-4">
      <label className="label-text">
        {label}:
        <select
          value={selectedValue}
          onChange={handleSelectChange}
          className="block w-full py-3 border border-slate-200 rounded-lg px-3 focus:outline-none focus:border-slate-500 hover:shadow dark:bg-gray-600 dark:text-gray-100"
        >
          {options.map((option) => (
            <option className="select-item" key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </label>
    </div>
  );
}

function AddProject() {
  const [name, setName] = useState("");
  const [summary, setSummary] = useState("");
  const [price, setPrice] = useState("");
  const [category, setCategory] = useState("minimum");

  const [docFile, setDocFile] = useState(null);
  const [coverFile, setCoverFile] = useState(null);
  const [pptxFile, setPptxFile] = useState(null);
  const [uniqueFile, setUniqueFile] = useState(null);
  const [productFile, setProductFile] = useState([]);

  useEffect(() => {
    async function getT() {
      await getToken();
    }
    getT();
  }, []);

  const navigate = useNavigate();
  const createProject = async (event) => {
    event.preventDefault();
    const data = {
      name: name,
      summary: summary,
      price: price,
      category: category,
      have_presentation: pptxFile ? true : false,
      have_unique: uniqueFile ? true : false,
      have_product: productFile.length != 0 ? true : false,
    };
    const files = {
      doc_file: docFile,
      cover_file: coverFile,
      pptx_file: pptxFile,
      unique_file: uniqueFile,
      product_files: productFile.length != 0 ? productFile : null,
    };
    const promise = addProject(data);
    promise.then((response) => {
      response.json().then((responseJson) => {
        const new_id = responseJson.new_id;
        addFiles(new_id, files).then(() => {
          navigate("/");
        });
      });
    });
  };
  return (
    <div id="add-project-page">
      <h1>BITCH</h1>
      <div className="">
        <form onSubmit={createProject} className="max-w-2xl">
          <div className="form-border flex flex-wrap shadow rounded-lg p-3 dark:bg-transparent-600">
            <h2 className="header-2-text text-xl pb-2">Добавить проект:</h2>

            <div className="flex flex-col gap-2 w-full border-gray-400">
              <InputField
                label="Название"
                value={name}
                onChange={(event) => {
                  setName(event.target.value);
                }}
              />
              <TextArea
                label="Краткое содержание"
                value={summary}
                onChange={(event) => {
                  setSummary(event.target.value);
                }}
              />
              <InputField
                label="Цена"
                value={price}
                onChange={(event) => {
                  setPrice(event.target.value);
                }}
              />
              <SelectFromListInput
                label="Категория"
                options={["minimum", "full11", "full9", "exclusive"]}
                onChange={(selectedValue) => {
                  setCategory(selectedValue);
                }}
              />

              <div className="flex files-combo">
                <UploadFile
                  name="Документ"
                  idSuffix="doc"
                  file={docFile}
                  setFile={setDocFile}
                />
                <UploadFile
                  name="Обложка"
                  idSuffix="cover"
                  file={coverFile}
                  setFile={setCoverFile}
                />
                <UploadFile
                  name="Презентация"
                  idSuffix="pptx"
                  file={pptxFile}
                  setFile={setPptxFile}
                />
                <UploadFile
                  name="Уникальность"
                  idSuffix="unique"
                  file={uniqueFile}
                  setFile={setUniqueFile}
                />
                <UploadFile
                  name="Продукт"
                  idSuffix="product"
                  file={productFile}
                  setFile={setProductFile}
                />
              </div>

              <div className="submit-button flex justify-end">
                <button
                  className="py-2 px-3 mt-4 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-500 focus:outline-none focus:shadow-outline-blue active:bg-blue-600 transition duration-150 ease-in-out"
                  type="submit"
                >
                  Создать
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AddProject;

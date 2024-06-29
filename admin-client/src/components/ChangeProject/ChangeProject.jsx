import React, { useState, useEffect } from "react";
import { changeProject, changeFiles } from "../../utils/changeProject";
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
      setFile([...files]);
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
            {file.length != 0 ? "П ✔️" : name}
          </span>
        ) : (
          <span className="label-text font-medium">
            {file ? name[0] + " ✔️" : name}
          </span>
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

function ChangeProject({ project }) {
  project.price = project.price.replace(" ₽", "");
  const [name, setName] = useState(project.name);
  const [summary, setSummary] = useState(project.summary);
  const [price, setPrice] = useState(project.price);
  const [category, setCategory] = useState(
    project.category.replace(/\s/g, "").toLowerCase()
  );
  const [isBlocked, setIsBlocked] = useState(project.is_blocked);

  const [docFile, setDocFile] = useState("HAVE");
  const [coverFile, setCoverFile] = useState("HAVE");
  const [pptxFile, setPptxFile] = useState(null);
  const [uniqueFile, setUniqueFile] = useState(null);
  const [productFile, setProductFile] = useState([]);
  useEffect(() => {
    if (project.have_product) {
      setProductFile("HAVE");
    }
    if (project.have_presentation) {
      setPptxFile("HAVE");
    }
    if (project.have_unique) {
      setUniqueFile("HAVE");
    }
  }, [project]);

  const createProject = async (event) => {
    event.preventDefault();
    const data = {
      name: name,
      summary: summary,
      price: price,
      category: category,
      is_blocked: isBlocked,
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
    const promise = changeProject(data, project.id);
    promise.then((response) => {
      response.json().then((responseJson) => {
        try {
          changeFiles(project.id, files).then((response) => {
            window.location.reload();
          });
        } catch {
          window.location.reload();
        }
      });
    });
  };
  return (
    <div className="change-project">
      <div className="grid">
        <form onSubmit={createProject} className="">
          <h2 className="header-2-text text-xl pb-2">Изменить проект:</h2>

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
                idSuffix="document"
                file={docFile}
                setFile={setDocFile}
              />
              <UploadFile
                name="Обложка"
                idSuffix="cover"
                file={coverFile}
                setFile={setCoverFile}
              />
            </div>
            <div className="flex files-combo">
              <UploadFile
                name="Уникальность"
                idSuffix="unique"
                file={uniqueFile}
                setFile={setUniqueFile}
              />
              <UploadFile
                name="Презентация"
                idSuffix="pptx"
                file={pptxFile}
                setFile={setPptxFile}
              />
              <UploadFile
                name="Продукт"
                idSuffix="product"
                file={productFile}
                setFile={setProductFile}
              />
            </div>

            <div className="flex justify-between">
              <button
                onClick={(event) => {
                  event.preventDefault();
                  setIsBlocked(!isBlocked);
                }}
                className={`py-2 px-8 mt-4 font-medium text-white ${
                  !isBlocked
                    ? "bg-green-600 rounded-md hover:bg-green-500 focus:outline-none focus:shadow-outline-green active:bg-green-600"
                    : "bg-red-600 rounded-md hover:bg-red-500 focus:outline-none focus:shadow-outline-red active:bg-red-600"
                } transition duration-150 ease-in-out`}
              >
                {isBlocked ? "Заблокировано" : "Разблокировано"}
              </button>
              <button
                className="py-2 px-8 mt-4 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-500 focus:outline-none focus:shadow-outline-blue active:bg-blue-600 transition duration-150 ease-in-out"
                type="submit"
              >
                Отправить изменения
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ChangeProject;

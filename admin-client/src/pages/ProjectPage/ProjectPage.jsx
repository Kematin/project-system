import React, { useEffect } from "react";
import ChangeProject from "../../components/ChangeProject/ChangeProject.jsx";
import ModalProject from "../../components/ModalProject/ModalProject.jsx";
import "./index.css";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { getProject, getFile } from "../../utils/getProjects.js";
import { deleteProject } from "../../utils/deleteProject.js";

function DownloadFile({ name, fileName, type, typeResponse, projectId }) {
  return (
    <button
      onClick={() => {
        getFile(fileName, type, typeResponse, projectId);
      }}
      className="px-4 py-2 flex gap-2 rounded-lg link-item"
    >
      {name}
    </button>
  );
}

function ListItem({ name, type }) {
  return (
    <li className="flex space-x-3">
      <svg
        className="flex-shrink-0 h-8 w-8 text-blue-600"
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M11.5219 4.0949C11.7604 3.81436 12.181 3.78025 12.4617 4.01871C12.7422 4.25717 12.7763 4.6779 12.5378 4.95844L6.87116 11.6251C6.62896 11.91 6.1998 11.94 5.9203 11.6916L2.9203 9.02494C2.64511 8.78033 2.62032 8.35894 2.86493 8.08375C3.10955 7.80856 3.53092 7.78378 3.80611 8.02839L6.29667 10.2423L11.5219 4.0949Z"
          fill="currentColor"
        />
      </svg>
      <span className="span-text">{type}: </span>
      <span className="text-gray-800 dark:text-gray-400">{name}</span>
    </li>
  );
}

function ProjectPage() {
  const [isModal, setModal] = React.useState(false);
  const [project, setProject] = React.useState(null);
  const navigate = useNavigate();
  const { id } = useParams();
  const files = [];

  function setProjectUrls(project) {
    if (project) {
      files.push({
        data: {
          name: "Скачать документ",
          type: "doc",
          fileName: "document.docx",
          typeResponse: "application/msword",
        },
      });
      files.push({
        data: {
          name: "Скачать обложку",
          type: "cover",
          fileName: "cover.png",
          typeResponse: "image/png",
        },
      });
      if (project.have_unique) {
        files.push({
          data: {
            name: "Скачать уникальность",
            type: "png",
            fileName: "unique.png",
            typeResponse: "image/png",
          },
        });
      }
      if (project.have_presentation) {
        files.push({
          data: {
            name: "Скачать презентацию",
            type: "pptx",
            fileName: "presentation.pptx",
            typeResponse: "application/vnd.ms-powerpoint",
          },
        });
      }
      if (project.have_product) {
        files.push({
          data: {
            name: "Скачать продукт",
            type: "product",
            fileName: "product.zip",
            typeResponse: "application/zip",
          },
        });
      }
    }
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const projectData = await getProject(id);
        setProject(projectData);
      } catch (error) {
        console.error("Error fetching project:", error);
      }
    };
    fetchData();
  }, [id]);

  if (!project) {
    return <div>Loading...</div>;
  } else {
    setProjectUrls(project);
  }

  return (
    <div className="project-page">
      <h1>{project.name}</h1>
      <ul className="space-y-3 text-lg border border-2 border-indigo-400 rounded-lg p-5">
        <ListItem type="ID" name={project.id} />
        <ListItem type="Краткое содержание" name={project.summary} />
        <ListItem type="Цена" name={project.price} />
        <ListItem type="Категория" name={project.category} />
        <ListItem type="Блок" name={project.is_blocked.toString()} />
        <ListItem
          type="Презентация"
          name={project.have_presentation.toString()}
        />
        <ListItem type="Продукт" name={project.have_product.toString()} />
        <ListItem type="Уникальность" name={project.have_unique.toString()} />
        <ListItem type="Дата создания" name={project.created_at} />
      </ul>
      <div className="flex justify-between">
        <button
          onClick={() => setModal(true)}
          className="px-4 py-2 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-500 focus:outline-none focus:shadow-outline-blue active:bg-blue-600 transition duration-150 ease-in-out"
        >
          Изменить
        </button>
        <button
          onClick={async () => {
            await deleteProject(id);
            navigate("/");
            window.location.reload();
          }}
          className="ml-1 px-4 py-2 font-medium text-white bg-red-600 rounded-md hover:bg-red-500 focus:outline-none focus:shadow-outline-red active:bg-red-600 transition duration-150 ease-in-out"
        >
          Удалить
        </button>
      </div>
      {files.map((data, index) => {
        data = data.data;
        return (
          <div key={index}>
            <DownloadFile
              name={data.name}
              type={data.type}
              fileName={data.fileName}
              typeResponse={data.typeResponse}
              projectId={id}
            />
          </div>
        );
      })}
      <ModalProject
        isVisible={isModal}
        title={`${project.name}`}
        content={<ChangeProject project={project} />}
        footer={<p>{project.created_at}</p>}
        onClose={() => setModal(false)}
      />
    </div>
  );
}

export default ProjectPage;

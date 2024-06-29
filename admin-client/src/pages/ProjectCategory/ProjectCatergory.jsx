import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import ProjectTable from "../../components/ProjectTable/ProjectTable.jsx";
import { getProjectsCategory } from "../../utils/getProjects.js";

function ProjectCatergory() {
  const { category } = useParams();
  const [projects, setProject] = useState(null);
  const navigate = useNavigate();
  useEffect(() => {
    const fetchData = async () => {
      try {
        const projectData = await getProjectsCategory(category);
        setProject(projectData);
      } catch (error) {
        navigate("/undefined");
      }
    };

    fetchData();
  }, [category]);

  if (!projects) {
    return <div>Loading...</div>;
  }
  return (
    <div className="projects-page">
      <ProjectTable projects={projects} />
    </div>
  );
}

export default ProjectCatergory;

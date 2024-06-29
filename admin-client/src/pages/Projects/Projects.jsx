import React, { useState, useEffect } from "react";
import { getProjects } from "../../utils/getProjects.js";
import ProjectTable from "../../components/ProjectTable/ProjectTable.jsx";

function Projects() {
  const [projects, setProject] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const projectData = await getProjects();
        setProject(projectData);
      } catch (error) {
        console.error("Error fetching project:", error);
      }
    };

    fetchData();
  }, []);

  if (!projects) {
    return <div>Loading...</div>;
  }
  return (
    <div className="projects-page">
      <ProjectTable projects={projects} />
    </div>
  );
}

export default Projects;

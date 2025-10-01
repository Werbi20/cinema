// Script para testar o backend
const fetch = require("node-fetch");

async function testBackend() {
  console.log("🧪 Testando backend...");

  try {
    // Testar endpoint de saúde
    const healthResponse = await fetch("http://localhost:8000/health");
    const healthData = await healthResponse.json();
    console.log("✅ Health check:", healthData);

    // Testar endpoint de locações
    const locationsResponse = await fetch(
      "http://localhost:8000/api/v1/locations/"
    );
    const locationsData = await locationsResponse.json();
    console.log("✅ Locações encontradas:", locationsData.length);

    // Testar endpoint de usuários
    const usersResponse = await fetch("http://localhost:8000/api/v1/users/");
    const usersData = await usersResponse.json();
    console.log("✅ Usuários encontrados:", usersData.length);

    // Testar endpoint de projetos
    const projectsResponse = await fetch(
      "http://localhost:8000/api/v1/projects/"
    );
    const projectsData = await projectsResponse.json();
    console.log("✅ Projetos encontrados:", projectsData.length);

    // Testar endpoint de locações de projetos
    const projectLocationsResponse = await fetch(
      "http://localhost:8000/api/v1/project-locations/"
    );
    const projectLocationsData = await projectLocationsResponse.json();
    console.log(
      "✅ Locações de projetos encontradas:",
      projectLocationsData.length
    );
  } catch (error) {
    console.error("❌ Erro ao testar backend:", error.message);
  }
}

testBackend();

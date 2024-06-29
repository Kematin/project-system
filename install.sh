# install api (check enviroment before start)
cd projects-api
docker build -t project_api .

# install admin panel
cd ..
cd admin-client
docker build -t admin_panel .

# install telegram bot
cd ..
cd sell-projects-bot
docker build -t project_bot .

# up container images
cd ..
docker-compose up -d
Installation steps
========================

    git clone https://github.com/ecosensvein/ush2.git
    cd ush2
    docker-compose up -d db
    docker-compose exec db mysql -u root -p -e 'CREATE DATABASE `ush` DEFAULT CHARACTER SET = `utf8mb4`'
    docker-compose down
    docker-compose up

Browse to [http://localhost:80](http://localhost:80)

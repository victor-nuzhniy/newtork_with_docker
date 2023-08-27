


Docker commands

1. Explore Docker containers file system
 - docker exec -it <container-hash> sh


Linux commands

1. Download docker-compose version to /usr/local/bin
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
2. Correct permission, make the docker-compose commands executable
    sudo chmod +x /usr/local/bin/docker-compose
3. Install docker
    sudo apt install apt-transport-https ca-certificates curl software-properties-common
4. Add the GPG key for the official Docker repository to your system
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
5. Add the Docker repository to APT sources
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
6. Make sure you are about to install from the Docker repo instead of the default Ubuntu repo
    apt-cache policy docker-ce
7. Install Docker
    sudo apt install docker-ce
8. Check docker running
    sudo systemctl status docker
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.hostname = "study-vm"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 20480
    vb.cpus = 4
  end

  config.vm.box = "ubuntu/bionic64"
  config.vm.box_check_update = false

  config.vm.network "forwarded_port", guest: 9000, host: 9000 #SonarQube
  config.vm.network "forwarded_port", guest: 8888, host: 8888 #JupyterLab (Password: sonar)

  config.vm.synced_folder ".", "/home/vagrant/study.d"

  config.vm.provision :docker
  config.vm.provision :docker_compose, 
      yml: "/home/vagrant/study.d/docker-compose.yml", 
      run: "always"

end

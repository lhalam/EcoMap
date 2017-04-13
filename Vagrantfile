# -*- mode: ruby -*-
# vi: set ft=ruby :

ENV['VAGRANT_DEFAULT_PROVIDER'] = 'virtualbox'

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/xenial64"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 3306, host: 8081

  config.vm.provider "virtualbox" do |vb|
  # # Display the VirtualBox GUI when booting the machine
  # # if needed
  # vb.gui = true
    vb.cpus = 2
    vb.memory = "2048"
  end
  # Comment next line to save ~ 200 Mb of disk space :)
  config.vm.provision "shell", path: "guestadditions.sh"

  config.vm.provision "docker" do |d|
    d.pull_images "ubuntu"
    d.pull_images "mariadb"
    d.build_image "/vagrant",
      args: "-t web"
    d.run "mariadb",
      cmd: "mysqld --character-set-server=utf8 --collation-server=utf8_unicode_ci --init_connect='SET collation_connection = utf8_unicode_ci'",
      args: "-p 3306:3306 -e MYSQL_ROOT_PASSWORD=megasecret -e MYSQL_DATABASE=ecomap"
    d.run "web",
      args: "-p 80:80 --link mariadb:mysql"
  end
end

# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"

    config.vm.synced_folder '/opt/collaborative_filtering', '/opt/collaborative_filtering'

    config.vm.network "forwarded_port", guest: 80, host: 8080

    config.vm.provider 'virtualbox' do |vbox|
        vbox.memory = 2048
        vbox.cpus = 2
    end

    config.vm.provision "ansible" do |ansible|
        ansible.playbook = "/opt/collaborative_filtering/deploy/ansible_playbook.yml"
    end
end

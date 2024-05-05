# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "kisp/archlinux"

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024 * 8
    v.cpus = `nproc`.to_i
  end

  # config.vm.network "forwarded_port", guest: 3000, host: 3000

  config.vm.provision "shell" do |s|
    s.name = "Upgrade system"
    s.privileged = false
    s.reboot = true
    s.inline = <<~SHELL
      sudo pacman -Sy archlinux-keyring --noconfirm --needed
      yay --noconfirm
      yay -S --noconfirm docker nix direnv
      sudo systemctl enable docker
      sudo systemctl enable nix-daemon
      sudo nix-channel --add https://nixos.org/channels/nixpkgs-unstable
      sudo nix-channel --update
      sudo usermod -a -G docker,nix-users vagrant
      echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
    SHELL
  end

  if ENV["GIT_USER_NAME"] && ENV["GIT_USER_EMAIL"]
    config.vm.provision "ansible" do |ansible|
      git_user_name = ENV["GIT_USER_NAME"]
      git_user_email = ENV["GIT_USER_EMAIL"]

      ansible.playbook = ".vagrant-ansible-provisioner-git-config.yml"
      ansible.raw_arguments = [
        "-e git_user_name='#{git_user_name}'",
        "-e git_user_email='#{git_user_email}'",
      ]
    end
  end
end

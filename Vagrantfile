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
end

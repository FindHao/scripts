#!/bin/bash

a7zversion="7z2400-linux-x64"
target_path=${target_path:-~/opt/7z}
if [ ! -d "$target_path" ]; then
    mkdir -p "$target_path"
fi
echo "7z installer -> Install 7z to $target_path"
cd "$target_path"
rm -f $a7zversion.tar.xz
wget -c "https://www.7-zip.org/a/$a7zversion.tar.xz"
tar -xf $a7zversion.tar.xz
rm -f $a7zversion.tar.xz
echo 7zpath to $PATH in ~/.bashrc and ~/.zshrc
echo "export PATH=$target_path:\$PATH" >> ~/.bashrc
echo "export PATH=$target_path:\$PATH" >> ~/.zshrc
echo "7z installer -> add 7zpath to \$PATH in ~/.bashrc and ~/.zshrc"
echo "source ~/.bashrc or source ~/.zshrc"

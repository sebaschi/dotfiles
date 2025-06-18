#!/bin/bash

source ./shellib/dot-local/lib/shellib/tasklib.sh

get_gnu_stow_latest_tar_gz() {
	wget --secure-protocol=auto https://ftpmirror.gnu.org/gnu/stow/stow-latest.tar.gz || {
		echo "Error: Failed to download GNU Stow" >&2
		return 1
	}
}

unpack_stow_tar_gz_archive() {
	if [[ ! -f "stow-latest.tar.gz" ]]; then
		echo "Error: stow-latest.tar.gz not found" >&2
		return 1
	fi
	tar xvf stow-latest.tar.gz
}

install_stow_latest_from_source() {
	local stow_dir=$(find . -name "stow-*" -type d | head -1)
	if [[ -z "$stow_dir" ]]; then
		echo "Error: Stow source directory not found" >&2
		return 1
	fi
	
	cd "$stow_dir" || return 1
	./configure --prefix="$HOME/.local" || return 1
	make || return 1
	make install || return 1
	cd - > /dev/null
}

install_gnu_stow() {
	if grep -q 'ID=fedora' /etc/os-release 2>/dev/null; then
		sudo dnf install -y stow
	else
		get_gnu_stow_latest_tar_gz && \
		unpack_stow_tar_gz_archive && \
		install_stow_latest_from_source
	fi
}


"@"

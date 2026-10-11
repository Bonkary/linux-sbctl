
install = ['sudo', 'pacman', '-Sy', 'sbctl', '--noconfirm']
create_keys = ['sudo', 'sbctl', 'create-keys']
enroll_keys = ['sudo', 'sbctl', 'enroll-keys', '--microsoft', '--firmware-builtin']
hash = []
hash_wallpaper = []
get_progress = []
is_installed = ['pacman', '-Q', 'sbctl']
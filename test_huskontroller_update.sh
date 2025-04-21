#!/usr/bin/env bash
cd "$(dirname "$0")"
husk_dir="$(pwd)/huskontroller"
husk_file="$(pwd)/huskontroller/Huskontroller.py"
backup_dir="$(pwd)/huskontroller-backup-$(date +%Y-%m-%d-%H-%M-%S)"
update_log="$(pwd)/update.log"

# Checks to see if huskontroller directory exists. If so:
# Backup the huskontroller directory and clone new version
if [ -d "$husk_dir" ]; then
	echo "Backing up $husk_dir to $backup_dir" >> $update_log
	mv "$husk_dir" "$backup_dir"
	git clone https://github.com/ccrader-uw/huskontroller.git
fi

# If the new version doesn't exist, restore from backup
if ![ -f "$husk_file" ]; then
	echo "Problem with update, restoring $husk_dir from $backup_dir" >> $update_log
	rm -r "$husk_dir"
	cp "$backup_dir" "$husk_dir"
	
fi

shutdown now -r

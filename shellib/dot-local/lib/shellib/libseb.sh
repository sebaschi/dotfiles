log() {
  # Write msg to stderr.
  # Taken from https://github.com/oils-for-unix/oils/blob/master/stdlib/osh/two.sh
  echo "$@" >&2
}

die() {
  # Write error msg with script name and exit with status 1.
  # Taken from https://github.com/oils-for-unix/oils/blob/master/stdlib/osh/two.sh
  log "$@: fatal $@"
  exit 1
}

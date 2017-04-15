#!/bin/bash
# run_fan.sh: To run (start/stop/status) raspberry pi fan service

##
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed WITHOUT ANY WARRANTY;
#  without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

SCRIPT_NAME='control_fan.py'
SCRIPT_DIR="/home/pi/scripts"
SCRIPT_PATH="${SCRIPT_DIR}/${SCRIPT_NAME}"
SCRIPT_EXEC="python ${SCRIPT_PATH}"
LOG_DIR="/var/log/custom_services"
LOG_NAME="run_fan_$(date +%s).log"
LOG_PATH="${LOG_DIR}/${LOG_NAME}"

# To check if service is running
get_status() {
  local status=
  pgrep -f "${SCRIPT_NAME}" > /dev/null 2>&1
  echo "$?"
}

# To get the pid of the script if running
get_pid() {
  local pid=
  pid=$(pgrep -f "${SCRIPT_NAME}")
  echo "${pid}"
}

print_status() {
  local status
  status=$(get_status)
  if [ $status -eq 0 ]; then
    local pid
    pid=$(get_pid)
    echo -e "${SCRIPT_NAME} running, pid: ${pid}"
  else
    echo "Not running"
  fi
  return "${status}"
}

start_service() {
  local status
  status=$(get_status)
  if [ $status -eq 0 ]; then
    local pid
    pid=$(get_pid)
    echo "Already running, pid: ${pid}"
    return 1
  fi

  # Run the script
  # Also check if script exists
  if [ -f "${SCRIPT_PATH}" ]; then
    # check for log dir
    [ ! -d "${LOG_DIR}" ] && mkdir -p "${LOG_DIR}"
    # now run the script
    ${SCRIPT_EXEC} > ${LOG_PATH} 2>&1 &
  else
    echo "Script not found"
    return 1
  fi

  local status
  status=$(get_status)
  if [ $status -eq 0 ]; then
    local pid
    pid=$(get_pid)
    echo "Service started, pid: ${pid}" >&2
  else
    echo "Unable to start"
    return 1
  fi
}

stop_service() {
  local pid=$(get_pid)
  if [ -n "${pid}" ]; then
    kill -9 "${pid}"
    if [ $? -eq 0 ]; then
      echo "Killed: ${pid}"
    fi
  else
    echo "Not running"
    return 1
  fi
}


case "$1" in
  start)
    start_service
    ;;
  stop)
    stop_service
    ;;
  status)
    print_status
    ;;
  restart)
    stop_service
    start_service
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status} [service-name]"
    echo "Default service name is ${SCRIPT_NAME} and path is ${SCRIPT_PATH}"
esac

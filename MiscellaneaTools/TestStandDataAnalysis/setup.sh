#!/bin/bash

# defaults
showHelpMsg=false
defScramArch=el8_amd64_gcc12
defCmssetDefault=/opt/offline/cmsset_default.sh

# help message
usage() {
  cat <<@EOF
Usage:
  This script sets up the SCRAM_ARCH and sources cmsset_default.sh.
  If the name of a CMSSW release is specified (option: -r),
  cmsenv is done in this release.

> source setup.sh [-h] [-a scram_arch] [-c cmsset_default.sh] [-r CMSSW_X_Y_Z]

  (square brackets denote optional arguments; do not use them when sourcing the script)

Options:
  -h, --help      Show this help message
  -a, --arch      Value of SCRAM_ARCH                [Default: ${defScramArch}]
  -c, --cmsset    Path to cmsset_default.sh script   [Default: ${defCmssetDefault}]
  -r, --release   Name of CMSSW release              [Optional]
@EOF
}

# command-line interface
scramArch=${defScramArch}
cmssetDefault=${defCmssetDefault}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) showHelpMsg=true; shift;;
    -a|--arch) scramArch=$2; shift; shift;;
    -c|--cmsset) cmssetDefault=$2; shift; shift;;
    -r|--release) cmsswRelease=$2; shift; shift;;
    *) shift;;
  esac
done

# clear transient variables/functions
clear_vars(){
  unset showHelpMsg defScramArch defCmssetDefault usage scramArch cmssetDefault cmsswRelease clear_vars
}

# print help message
if [ ${showHelpMsg} == true ]; then
  usage
  clear_vars
  return 0
fi

# set up environment
printf "\033[1m%s\033[0m%s\n" "SCRAM Architecture" "       : ${scramArch}"
printf "\033[1m%s\033[0m%s\n" "cmsset_default.sh script" " : ${cmssetDefault}"

if [ ! -f "${cmssetDefault}" ]; then
  printf "\n\033[31m\033[1m%s\033[0m%s\n\n" ">> ERROR" ": invalid path to cmsset_default.sh script [-c]: ${cmssetDefault}"
  usage
  clear_vars
  return 1
fi

export http_proxy="http://cmsproxy.cms:3128/"
export https_proxy="http://cmsproxy.cms:3128/"
export NO_PROXY=".cms,localhost"

export SCRAM_ARCH=${scramArch}
export USER_SCRAM_TARGET=x86-64-v3

source ${cmssetDefault}

export TZ='-01:00'

# do cmsenv in the release installation directory
if [ ! -z "${cmsswRelease}" ]; then
    printf "\033[1m%s\033[0m%s\n" "CMSSW Release" "            : ${cmsswRelease}"
    cmsswBase=`scram list -c CMSSW | grep "\<$cmsswRelease\>" | awk '{ print $3; }'`
    if ! [ "${cmsswBase}" ]; then
        printf "\n%s\n" "CMSSW release ${cmsswRelease} is not installed for the architecture ${SCRAM_ARCH}."
        scram list CMSSW
        clear_vars
        return 1
    elif ! [ -d "${cmsswBase}" ]; then
        printf "\n%s\n" "The directory ${cmsswBase} does not exist; the release installation is probably broken."
        clear_vars
        return 1
    else
        printf "\n%s\n" "Setting up the CMSSW environment from ${cmsswBase}"
        cd ${cmsswBase}
        eval `scram runtime -sh`
        cd ${OLDPWD}
        printf "\033[34m\033[1m%s\033[0m=%s\n" "CMSSW_BASE" "${CMSSW_BASE}"
    fi
    unset cmsswRelease cmsswBase
else
  printf "\n%s\n" "Did not set up CMSSW environment (to do this, specify the name of a release via option -r)"
  printf "\033[34m\033[1m%s\033[0m=%s\n" "CMSSW_BASE" "${CMSSW_BASE}"
fi

clear_vars

#!/bin/bash
# To use make set as a git alias
# git config --global alias.cleanup '!sh .tools/git-cleanup.sh'
# Usage: 
#   git cleanup local
#   git cleanup remote
#   --dry-run to show which branches would be deleted
#   --unmerged when running "remote" to remove unmerged branches too


lstring="To delete local branches manually you could use:
git branch -d <branch-name>"
rstring="To delete remote branches manually you could use:
git push --delete origin <branch-name>"

DRYRUN=0
for i in "$@" ; do [ $i = "--dry-run" ] && DRYRUN=1 && break ; done

UNMERGED=0
for i in "$@" ; do [ $i = "--unmerged" ] && UNMERGED=1 && break ; done
MERGED=$((1-$UNMERGED))

if [ $USER != anovak ]; then 
  echo "Don't do that. If you insist, change lins 23-25 in .tools/git-cleanup.sh"
  exit 1
fi

if [ "$1" =   "local" ]; then
  if [ $DRYRUN = 1 ]; then
    echo "Would delete the following local branches:"
    git branch --merged | egrep -v "(^\*|master|dev)" 
    echo $lstring
  else
    echo "Will delete the following local branches:"
    git branch --merged | egrep -v "(^\*|master|dev)" 
    echo $lstring
    
    read -r -p "Are you sure? [Y/n]" CONT
    # if [ "$CONT" = "y" ] || [ -z $CONT ]; then # To allow enter
    if [ "$CONT" = "y" ] || [ -z $CONT ]; then
      git branch --merged | egrep -v "(^\*|master|dev)" | xargs git branch -d
    else
      echo
      echo "No action taken";
      echo
    fi
  
  fi
elif [ "$1" = "remote" ]; then
  if [ $DRYRUN = 1 ]; then
    echo "Would delete the following remote branches:"
    if [ $MERGED = "1" ]; then
      git branch -r --merged | egrep -v "(^\*|/master|dev)" 
    else
      git branch -r | egrep -v "(^\*|/master|dev)" 
    fi
    echo $rstring
  else 
    echo "Will delete the following remote branches:"
    if [ $MERGED ]; then
      git branch -r --merged | egrep -v "(^\*|/master|dev)" 
    else
      git branch -r | egrep -v "(^\*|/master|dev)" 
    fi
    echo $rstring

    read -r -p "Are you sure? [Y/n]" CONT
    # if [ "$CONT" = "y" ] || [ -z $CONT ]; then # To allow enter
    if [ "$CONT" = "y" ] || [ -z $CONT ]; then
      if [ $MERGED ]; then
        git branch -r --merged | egrep -v "(^\*|/master|dev)" | awk -F/ '{print $NF}' | xargs -n 1 git push --delete origin
      else
        git branch -r | egrep -v "(^\*|/master|dev)" | awk -F/ '{print $NF}' | xargs -n 1 git push --delete origin
      fi
    else
      echo
      echo "No action taken";
      echo
    fi
  fi

else
  echo "git cleanup: $1 is not a valid git-cleanup option. See 'git cleanup --help'."
  echo $lstring
  echo $rstring

fi
#!/bin/bash
# To use make set as a git alias
# git config --global alias.cleanup '!sh .tools/git-cleanup.sh'
# Usage:
#   git cleanup local
#   git cleanup remote
#   --dryrun to show which branches would be deleted
#   --unmerged when running "remote" to remove unmerged branches too


lstring="To delete local branches manually you could use:
git branch -d <branch-name>"
rstring="To delete remote branches manually you could use:
git push --delete origin <branch-name>"

#### Opt Parsing
DRYRUN=0
for i in "$@" ; do [ $i = "--dryrun" ] && DRYRUN=1 && break ; done

UNMERGED=0
for i in "$@" ; do [ $i = "--unmerged" ] && UNMERGED=1 && break ; done
MERGED=$((1-$UNMERGED))
####

if [ $USER != anovak ]; then
  echo "Don't do that. If you insist, change lines 23-26 in .tools/git-cleanup.sh"
  exit 1
fi

if [ "$1" =   "local" ]; then
  echo  $([ $DRYRUN = 1  ] && echo "Would" || echo "Will") "delete the following local branches:"
  git branch $([ $MERGED = 1  ] && echo "--merged" || echo "") | egrep -v "(^\*|master|dev)"
  echo $lstring

  if [ $DRYRUN = 0 ]; then
    read -r -p "Are you sure? [y/n]" CONT
    if [ "$CONT" = "y" ] || [ -z $CONT ]; then
      git branch $([ $MERGED = 1  ] && echo "--merged" || echo "") | egrep -v "(^\*|master|dev)" | xargs git branch $([ $MERGED = 1  ] && echo "-d" || echo "-D")
    else
      echo
      echo "No action taken";
      echo
    fi

  fi
elif [ "$1" = "remote" ]; then
  echo  $([ $DRYRUN = 1  ] && echo "Would" || echo "Will") "delete the following remote branches:"
  git branch -r $([ $MERGED = 1  ] && echo "--merged" || echo "") | egrep -v "(^\*|master|dev)"
  echo $lstring

  if [ $DRYRUN = 0 ]; then
    read -r -p "Are you sure? [y/n]" CONT
    if [ "$CONT" = "y" ] || [ -z $CONT ]; then
      git branch -r $([ $MERGED = 1  ] && echo "--merged" || echo "") | egrep -v "(^\*|master|dev)" | awk -F/ '{print $NF}' | xargs -n 1 git push --delete origin
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

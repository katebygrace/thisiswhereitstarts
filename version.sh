#!/bin/sh


result=""
env -i
FILE=$(git describe --contains | cut -d$'\n' -f1)
echo $FILE #| cut -d " " -f1
if [[ $FILE == "" ]]; then 
    #bitrise doesn't really check out correctly so check out the right branch    

    export gitStatusOld=`git status`
    echo $gitStatusOld

    export gitBranch=`git switch -c $BITRISE_GIT_BRANCH`
    echo $gitBranch

    export gitStatusNew=`git status`
    echo $gitStatusNew

    #Tell the user we're version bumping 
    result="There is no tag. Running version bump and making a tag now"
    echo $result
    
    #get the marketing version output
    export wholeOutput=`xcrun agvtool what-marketing-version`
    echo $wholeOutput

 	#get the whole version number
 	export oldTag=`echo $wholeOutput | grep Cameras | cut -d '"' -f2`
    echo $oldTag
    
    #get the first part of the version number for safekeeping
    export majorVersionNumber=`echo $oldTag | cut -d '.' -f1`
    echo $majorVersionNumber

    #cut just the minor version we need
    export minorVersionNumber=`echo $oldTag | cut -d '.' -f2`
    echo $minorVersionNumber
    
    #BUMP IT  
    export newMinorNumber=$(($minorVersionNumber+1))
    echo $newMinorNumber

    #assemble new version number 
    export newVersionNumber="$majorVersionNumber.$newMinorNumber.0"
    echo $newVersionNumber

    #version bump 
    export wholeOutput=`xcrun agvtool new-marketing-version $newVersionNumber`
    echo $wholeOutput

    #git tag new version number
    git tag $newVersionNumber

    #git status
    export gitStatus=`git status`
    echo $gitStatus
    
    #get branch only 
    export gitBranch=`echo $gitStatus | cut -d ' ' -f3`
    echo $gitBranch

    #try checking out to the right freaking place
    export checkout=`git checkout $gitBranch`
    echo $checkout

    #git add and commit and push
    git add . 
    git commit -m "version bump to $newVersionNumber"
    git push origin HEAD:$gitBranch

else
    result="There is a tag. Not executing version bump, exiting"  
    echo $result
fi


#!/usr/bin/env bash
txtred='\e[00;31m' # Red
txtgrn='\e[00;32m' # Green
txtylw='\e[00;33m' # Yellow
txtpur='\e[0;35m'  # Purple
txtrst='\e[00m'    # Text Reset
function success() {
    echo -e ${txtgrn}$1${txtrst};
}
function info() {
    echo -e ${txtylw}$1${txtrst};
}
function warn() {
    echo -e ${txtpur}$1${txtrst};
}
function error() {
    echo -e ${txtred}$1${txtrst};
}
function run() 
{
    # Run the command
    info "Running: $1"
    eval $1
    # Check if it succeeded
    if [ "$?" != 0 ]; then
        error "$1 [FAILED]"
        exit 1
    else
        success "$1 [OK]"
    fi
}

virtualenv env
source env/bin/activate
success 'virtualenv activated'

pip install -e bzr+lp:~adam.russell/pyexiv2/pyexiv2-0.3#egg=pyexiv2
run "easy_install -Z hachoir-core"
run "easy_install -Z hachoir-metadata"
run "easy_install -Z hachoir-parser"
#run "easy_install hachoir-editor"

info "Manually getting hachoir-editor"
hachoir_repo="./third_party/hachoir"
if [ -d $hachoir_repo ]; then
	echo "hg update haypo/hachoir..."
	cd $hachoir_repo
	hg update
	cd - > /dev/null 2>&1
else
	echo "hg clone haypo/hachoir..."
	hg clone https://bitbucket.org/haypo/hachoir $hachoir_repo
fi

hachoir_editor="./env/lib/python2.7/site-packages/hachoir_editor/"
if [ -d $hachoir_editor ]; then
	rm -rf $hachoir_editor
fi
echo "Copying hachoir-editor to site-packages"
cp -R $hachoir_repo/hachoir-editor/hachoir_editor $hachoir_editor
success "Done"

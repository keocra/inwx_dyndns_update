export INWX_REPO=https://github.com/inwx/python2.7-client.git
export COMMIT_HASH=af81cb860b9226354efc8984de08ad101795227d
export LIB_FOLDER=inwx_managed_python_lib

echo "Cloning the inwx managed python library to $LIB_FOLDER..."
git clone $INWX_REPO $LIB_FOLDER

echo "Changing to Commit #$COMMIT_HASH so we'll get the version which was tested with this script..."
cd $LIB_FOLDER
git checkout $COMMIT_HASH

echo "Adding __init__.py to make it loadable module..."
touch __init__.py

echo "Removing git control..."
rm -rf ./.git

unset INWX_REPO
unset COMMIT_HASH
unset LIB_FOLDER

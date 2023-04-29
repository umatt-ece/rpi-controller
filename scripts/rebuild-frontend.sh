#!/bin/sh

# NOTE: to run this script use 'bash scripts/rebuild-frontend.sh' from ./rpi-controller
echo installing dependencies...

cd display
npm install

echo rebuilding frontend...

npm run build

echo moving files to server/vue-app...

rm -r ../server/vue-app/*
mv dist/* ../server/vue-app

echo rebuild finished!

# If you have issues with 'git pull' after using this script you can use 'git reset --hard' to hopefully fix it
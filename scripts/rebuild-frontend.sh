#!/bin/sh
# USAGE: run 'bash scripts/rebuild-frontend.sh' from ./rpi-controller

echo installing dependencies...

cd display
npm install

echo rebuilding frontend...

npm run build

echo moving files to server/vue-app...

rm -r ../server/vue-app/*
mv dist/* ../server/vue-app

echo rebuild finished!

# NOTE: If you have issues with 'git pull' after using this script due to the package-lock.json being updated, you
# can use 'git reset --hard' to reset the repository (may affect frontend build tho).

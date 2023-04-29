#!/bin/sh

# NOTE: to run this script use 'bash scripts/rebuild-frontend.sh' from ./rpi-controller
echo building frontend...

cd display
npm run build
mv dist/* ../server/vue-app

echo rebuild successful!

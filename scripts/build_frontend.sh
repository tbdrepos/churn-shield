#!/usr/bin/env bash
set -e

cd frontend
npm install
npm run build

rm -rf ../backend/static
mv dist ../backend/static

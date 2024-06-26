#!/bin/bash

die () { echo "ERROR: $*" >&2; exit 2; }

for cmd in pdoc3; do
    command -v "$cmd" >/dev/null ||
        die "Missing $cmd; \`pip install $cmd\`"
done

PACKAGE="plottools"
PACKAGESRC="src/$PACKAGE"
PACKAGEROOT="$(dirname "$(realpath "$0")")"
BUILDROOT="$PACKAGEROOT/site"
APIIMAGEFOLDER='figures'
APIIMAGES="$PACKAGEROOT/docs/$APIIMAGEFOLDER"

echo
echo "Clean up documentation of $PACKAGE"
echo

rm -rf "$BUILDROOT" 2> /dev/null || true
mkdir -p "$BUILDROOT"

echo "Building general documentation for $PACKAGE"
echo

cd "$PACKAGEROOT"
mkdocs build --config-file .mkdocs.yml --site-dir "$BUILDROOT" 
cd - > /dev/null

echo
echo "Building API reference docs for $PACKAGE"
echo

cd "$PACKAGEROOT"
pdoc3 --html --config sort_identifiers=False --output-dir "$BUILDROOT/api-tmp" $PACKAGESRC
mkdir "$BUILDROOT/api-tmp/$PACKAGE/$APIIMAGEFOLDER"
cp "$APIIMAGES/"*.png "$BUILDROOT/api-tmp/$PACKAGE/$APIIMAGEFOLDER/"
mv "$BUILDROOT/api-tmp/$PACKAGE" "$BUILDROOT/api"
rmdir "$BUILDROOT/api-tmp"
cd - > /dev/null

echo
echo "Done. Docs in:"
echo
echo "    file://$BUILDROOT/index.html"
echo
echo "Check with:"
echo
echo "    mkdocs serve -f .mkdocs.yml"
echo

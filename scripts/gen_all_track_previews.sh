#!/bin/sh

if [ $# -eq 0 ]; then
    echo "ERROR - Missing argument: Provide the path to the Assetto Corsa content/tracks folder."
    exit 1
fi

# e.g.: `/SteamLibrary/steamapps/common/assettocorsa/`
assettoTrackPath="${1}/content/tracks/"
# TODO fix relative path
imageOutPath=../plotlyflask/plotlydash/assets/img/

# TODO Add function (Use `acu_hungaroring` as local example modded map):
: '
#    1) Search for map: .../tracks/[map]/[map].kn5
#    2) Search for layout: .../tracks/[map]/models_layout_[layout].ini
# This way modded maps are supported
'
function createPreview() {
    magick composite -gravity center $assettoTrackPath/$1/ui/outline.png $assettoTrackPath/$1/ui/preview.png $imageOutPath/$1.png
}
function createLayoutPreview() {
    magick composite -gravity center $assettoTrackPath/$1/ui/$2/outline.png $assettoTrackPath/$1/ui/$2/preview.png $imageOutPath/$2.png
}

### Gen Single-Layout Tracks ###
# Find maps w/o different setups
for i in $(find $assettoTrackPath -name "models.ini" | sed -rn "s/.*\/content\/tracks\/([^\/]+)\/models(.*)\.ini/\1 \2/gp"); do
    createPreview $i
done

### Gen Multi-Layout Tracks ###
# Find maps w/ different setups
# TODO Fix extra whitespace
testDat="$(find $assettoTrackPath -name "models_*.ini" | sed -rn "s/.*\/content\/tracks\/([^\/]+)\/models_(.*)\.ini/\1 \2/gp")"
readarray -d ' ' test < <(echo $testDat)

i=0
arrayCount=${#test[@]}
#for i in "${test[@]}"; do
until [ $i -ge $arrayCount ]; do
    # Trim white spaces
    track=$(echo "${test[$i]}" | sed -e 's/  *$//')
    layout=$(echo "${test[$i+1]}" | sed -e 's/  *$//')

    echo $i: $track - $layout
    createLayoutPreview $track $layout
    ((i=i+2))
done


#!/bin/bash

audioPath=$1
videoPath=$2
delay=$3 # delay in seconds

# Check if audioPath is not empty
if [[ -z "$audioPath" ]]; then
  read -p "path to audio file: " audioPath
fi
# Check if videoPath is not empty
if [[ -z "$videoPath" ]]; then
  read -p "path to video file: " videoPath
fi

currentTime=$(date +"%H-%M-%S")
outputFileName="combined_$currentTime.mp4"
outputFilePath="./outputs/combined/$outputFileName"
# create directory if it doesn't exist already
[ -d "./outputs/combined" ] || mkdir -p "./outputs/combined"

callFFMPEG() {
  ffmpeg -i $videoPath -ss $delay -i "$audioPath" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest $outputFilePath
}

callFFMPEG

echo "$outputFilePath"


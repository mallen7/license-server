#!/bin/bash

cd lambda-functions

for dir in */ ; do
    func_name=${dir%/}  # Extract the function name from the directory name
    cd "$func_name"
    echo "Zipping ${func_name}..."
    zip -r "../${func_name}.zip" .
    cd ..
done

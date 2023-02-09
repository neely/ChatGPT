# Get the current directory where the script is run
$folder = Get-Location

# Get the files in the current directory
$files = Get-ChildItem -Path $folder

# Set the total number of sets of copies to create
$totalSets = 3

# Create a counter to use as the prefix for each set of copies
$counter = 1

# Loop through the total number of sets
for ($i = 0; $i -lt $totalSets; $i++) {
    # Generate the number to use as the prefix for this set of copies
    $number = "{0:D2}" -f $counter

    # Create a new folder for this set of copies
    New-Item -ItemType Directory -Path "$folder\$number"

    # Loop through each file in the folder
    foreach ($file in $files) {
        # Check the file extension and only continue if it's not .ps1
        if ($file.Extension -ne ".ps1") {
            # Generate the new file name by prefixing the number
            $newFileName = "$number-$file"

            # Make a copy of the file with the new name and move it to the new folder
            Copy-Item -Path $file.FullName -Destination "$folder\$number\$newFileName"
        }
    }

    # Increment the counter for the next set of copies
    $counter++
}

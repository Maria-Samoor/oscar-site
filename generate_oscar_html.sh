#!/bin/bash

mkdir -p Years Names

echo "<html><body><h1>Oscar Winners by Year</h1><ul>" > Years/index.html
echo "<html><body><h1>Oscar Winners by Name</h1><ul>" > Names/index.html

jq -c '.[]' oscar_age_gender.json | while read -r entry; do
    year=$(echo "$entry" | jq -r '.Year')
    name=$(echo "$entry" | jq -r '.Name')
    age=$(echo "$entry" | jq -r '.Age')
    movie=$(echo "$entry" | jq -r '.Movie')
    gender=$(echo "$entry" | jq -r '.Gender')

    entry_html="<li>${name} (${age}, ${gender}) - ${movie}</li>"
    actor_entry_html="<li>${movie} -(${age}, ${gender})</li>"

    echo "$entry_html" >> "Years/${year}_temp.txt"

    actor_filename=$(echo "$name" | tr ' ' '_')
    echo "$actor_entry_html" >> "Names/${actor_filename}_temp.txt"
done

for year_file in $(ls Years/*_temp.txt 2>/dev/null); do
    year=$(basename "$year_file" | cut -d'_' -f1)
    {
        echo "<html><body><h1>Oscar Winners for ${year}</h1><ul>"
        cat "$year_file"
        echo "</ul></body></html>"
    } > "Years/${year}.html"
    
    echo "<li><a href=\"${year}.html\">${year}</a></li>" >> Years/index.html
    
    rm "$year_file"
done

for actor_file in $(ls Names/*_temp.txt 2>/dev/null); do
    actor_filename=$(basename "$actor_file" | sed 's/_temp.txt//')
    actor_name=$(echo "$actor_filename" | tr '_' ' ')
    {
        echo "<html><body><h1>${actor_name}</h1><ul>"
        cat "$actor_file"
        echo "</ul></body></html>"
    } > "Names/${actor_filename}.html"
    
    echo "<li><a href=\"${actor_filename}.html\">${actor_name}</a></li>" >> Names/index.html
    rm "$actor_file"
done

echo "</ul></body></html>" >> Years/index.html
echo "</ul></body></html>" >> Names/index.html

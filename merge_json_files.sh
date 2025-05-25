#!/bin/bash
source config.env
# download the json files using wget, -q for quiet mode in order not to output anything in the terminal, and -O for the output file name
download_files() {
   wget -q -O tmp_female.json "$FEMALE_URL"
   wget -q -O tmp_male.json "$MALE_URL"
}

# add gender field directly using map function where key is Gender and Value is F or M based on the file name
add_gender_fields() {
  jq 'map(.Gender = "F")' tmp_female.json > tmp_female_with_gender.json
  jq 'map(.Gender = "M")' tmp_male.json > tmp_male_with_gender.json
}

# merge the 2 files based on the year and gender
merge_and_sort() {
  jq -s 'add | sort_by(.Year, .Gender)' tmp_female_with_gender.json tmp_male_with_gender.json > tmp_merged_sorted.json
}

# edit the index on the merged file and update the index
edit_index() {
  jq 'to_entries | map(.value.Index = (.key + 1) | .value)' tmp_merged_sorted.json > oscar_age_gender.json
}

# remove temp files
remove_files() {
  rm -f tmp_female.json tmp_male.json tmp_female_with_gender.json tmp_male_with_gender.json tmp_merged_sorted.json
}

download_files
add_gender_fields
merge_and_sort
edit_index
remove_files


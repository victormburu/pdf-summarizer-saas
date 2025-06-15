#!/bin/bash

>oldFile.txt
fils=$(grep "Alice" ../github/company_contacts.txt | cut -d ' ' -f 4);
for file in $files; do
 if test -e "..${file}"; then echo "..${file}" >> oldfile.txt; fi
done

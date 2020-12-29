echo "Cleaning directories if they exists"
./clean.sh
# this program is to make some tests to check if the encoding and decoding is working or not
echo -e "\n\n **** Starting tests **** \n"
echo "Running test 1. No args given"
python3 encode.py -d
python3 decode.py -d
# bydefault it expects input to be in testit folder and outputs encrypted folder
# bydefault encrypted files are decoded and stored in decrypted folder 
echo -e "\nResult for test 1 (If empty or only has files which are not in supported formats in encode, then successful)"
# diff command will check difference in files, and can even detect if any byte is different in files with same name
# if this is empty, it means all the files matched in two directories. If not, it will show which files not matching.
diff testit decrypted/testit
rm -r encrypted 
rm -r decrypted


echo -e "\nRunning test 2. Input and output directory mentioned"
cp -r testit temp_dir
python3 encode.py temp_dir enc_files -d
python3 decode.py enc_files dec_files -d
# temp_dir -> enc_files -> dec_files
echo -e "\nResult for test 2 (If empty or only has files which are not in supported formats in encode, then successful)"
diff temp_dir dec_files/temp_dir
rm -r enc_files
rm -r dec_files


echo -e "\nRunning test 3. Input and output directory mentioned with flags"
python3 encode.py temp_dir enc_files -cs 5000000 -k 27 -d
python3 decode.py enc_files dec_files -d
# temp_dir -> enc_files -> dec_files
echo -e "\nResult for test 3 (If empty or only has files which are not in supported formats in encode, then successful)"
diff temp_dir dec_files/temp_dir
rm -r enc_files
rm -r dec_files


echo -e "\nRunning test 4. Input and output directory mentioned with flags and password protected"
python3 encode.py temp_dir enc_files -cs 5000000 -k 27 -p -d
python3 decode.py enc_files dec_files -d
# temp_dir -> enc_files -> dec_files
echo -e "\nResult for test 4 (If empty or only has files which are not in supported formats in encode, then successful)"
diff temp_dir dec_files/temp_dir
rm -r enc_files
rm -r dec_files

echo -e "\nRunning test 5. Classifying images"
python3 encode.py temp_dir enc_files -f images -d
python3 decode.py enc_files Images_from_folder -d
rm -r enc_files

echo -e "\nRunning test 6. Classifying videos"
python3 encode.py temp_dir enc_files -f videos -d
python3 decode.py enc_files Videos_from_folder -d
rm -r enc_files

echo -e "\nRunning test 7. Classifying docs"
python3 encode.py temp_dir enc_files -f docs -d
python3 decode.py enc_files Documents_from_folder -d
rm -r enc_files

echo -e "\nRunning test 8. Classifying programs"
python3 encode.py temp_dir enc_files -f prog -d
python3 decode.py enc_files Programs_from_folder -d
rm -r enc_files
rm -r temp_dir
# add new tests here
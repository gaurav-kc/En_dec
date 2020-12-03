
# no input foldername given
rm -r encrypted 
rm -r decrypted
echo "Running test 1. No args given"
python3 encode.py
python3 decode.py
# bydefault it expects input to be in testit folder and outputs encrypted folder
# bydefault encrypted files are decoded and stored in decrypted folder 
echo -e "\nResult for test 1"
diff testit decrypted
rm -r encrypted 
rm -r decrypted


echo -e "\nRunning test 2. Input and output directory mentioned"
cp -r testit temp_dir
python3 encode.py temp_dir enc_files
python3 decode.py enc_files dec_files
# temp_dir -> enc_files -> dec_files
echo -e "\nResult for test 2"
diff temp_dir dec_files
rm -r enc_files
rm -r dec_files


echo -e "\nRunning test 3. Input and output directory mentioned with flags"
python3 encode.py temp_dir enc_files -cs 50000 -k 27
python3 decode.py enc_files dec_files
# temp_dir -> enc_files -> dec_files
echo -e "\nResult for test 3"
diff temp_dir dec_files
rm -r enc_files
rm -r dec_files


echo -e "\nRunning test 4. Input and output directory mentioned with flags and password protected"
python3 encode.py temp_dir enc_files -cs 50000 -k 27 -p
python3 decode.py enc_files dec_files
# temp_dir -> enc_files -> dec_files
echo -e "\nResult for test 4"
diff temp_dir dec_files
rm -r temp_dir
rm -r enc_files
rm -r dec_files
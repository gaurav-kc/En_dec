rm -r encrypted
rm -r decrypted
rm -r temp_dir
rm -r enc_files
rm -r dec_files
rm -r Images_from_folder
rm -r Videos_from_folder
rm -r Documents_from_folder
rm -r Programs_from_folder
# specify other directories you want to remove as argument to this script
for i in $*; do
    rm -r $i
done
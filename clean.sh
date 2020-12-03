rm -r encrypted
rm -r decrypted
for i in $*; do
    rm -r $i
done
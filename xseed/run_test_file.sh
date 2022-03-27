# ./run_test_file.sh [dir name] [name of conda env] [number of times to run tests] [full path to test command file] [suffix] [threads]
export LC_ALL=en_US.UTF-8
if [ "$#" -ne 6 ];
then
  echo "usage: ./run_tests.sh [dir name] [name of conda env] [number of times to run tests] [full path to test command file]"
  exit 1
fi

cd $1

source ~/anaconda3/etc/profile.d/conda.sh
conda activate $2
threads=$6
EPOCH_TIME=`date +'%s'`
DIR_NAME="${2}_${EPOCH_TIME}_${5}"

mkdir $DIR_NAME

#i=0
#while [ $i -lt $3 ]
#do
#  timeout 3600 $4 > "${DIR_NAME}/${i}.txt"
#  i=$(($i + 1))
#done
seq 1 $3 | parallel -j $threads "$4 $DIR_NAME {}"
conda deactivate
cd -

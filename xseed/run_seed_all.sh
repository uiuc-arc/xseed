#!/usr/bin/env bash
export LC_ALL=en_US.UTF-8
# ./run_all.sh [slug] [num times to run]



RunTests () {
  threads=$5
  scripts_dir=$4
  num_runs=$3
  conda_env=$2
  dir_path=$1

  # normal run
  $scripts_dir/run_test_file.sh $dir_path $conda_env $num_runs $scripts_dir/test_command.sh "wseed" $threads

  # run without seeds
  python3 $scripts_dir/remove_seeds_script.py "seed-test" $dir_path 

  $scripts_dir/run_test_file.sh $dir_path $conda_env $num_runs $scripts_dir/test_command.sh "woseed" $threads
}

CreateReport () {
  scripts_dir=$3
  conda_env=$2
  dir_path=$1
  name=$4
  # create final report
  cd $dir_path

  final_report="final_report_for_test_runs_${conda_env}_"
  final_report_dir="final_report_and_logs_for_test_runs_${conda_env}_"
  
  rm -rf $final_report_dir
  mkdir $final_report_dir

  relevant_dirs=`git status --short | cut -d'/' -f 1 | cut -d' ' -f 2 | grep "^${conda_env}_" | xargs echo`
  relevant_dir1=`echo $relevant_dirs | cut -d' ' -f 1`
  relevant_dir2=`echo $relevant_dirs | cut -d' ' -f 2`
  echo "Re dir 1: $relevant_dir1"
  python3 $scripts_dir/printFailedTestDiff.py $relevant_dir1 >> $final_report
  printf "\n*******\n" >> $final_report
  echo "Re dir 2: $relevant_dir2"
  python3 $scripts_dir/printFailedTestDiff.py $relevant_dir2 >> $final_report

  mv $final_report $final_report_dir
  mv $relevant_dir1 $relevant_dir2 $final_report_dir
  mv ../commit.txt ../evalreqs.txt ../${conda_env}_install_log.txt $final_report_dir  
  cd - > /dev/null
}


slug=$1
num_runs=$2
threads=$3

locale

mkdir -p logs
mkdir -p ../projects
random=$RANDOM
echo "Running ${slug}"

# install libs and dependencies
conda_env=`echo $slug | cut -d'/' -f 2`
name=`echo $slug | sed 's/\//_/'`


./general_setup.sh `realpath ../projects` $slug 'global'
dir_path=`realpath ../projects/${conda_env}`
RunTests $dir_path $conda_env $num_runs `realpath .` $threads
CreateReport $dir_path $conda_env `realpath .` $name




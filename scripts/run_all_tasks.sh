voting_threshold_settings=("simple_majority" "2_3_majority" "veto_power")
task_settings=("seat_apportionment" "rawlsianism" "utilitarianism") 
party_nums=(2 4 6)
eval_topics=("development" "culture & education" "agriculture" "gender equality" "regional development" "constitutional and inter-institutional affairs" "transport & tourism" "legal affairs" "employment & social affairs" "industry, research & energy" "fisheries" "internal market & consumer protection" "international trade" "budget" "environment & public health" "economic & monetary affairs" "civil liberties, justice & home affairs" "foreign & security policy" "budgetary control")

model_paths=("/.cache/Qwen/Qwen2.5-32B-Instruct" "/.cache/Qwen/Qwen2.5-72B-Instruct" "/.cache/meta-llama/Llama-3.3-70B-Instruct" "gemini-2.5-flash-preview" "gpt-4o" "deepseek-r1")

total_tasks=$((${#model_paths[@]} * ${#eval_topics[@]} * ${#party_nums[@]} * (${#task_settings[@]} + ${#voting_threshold_settings[@]})))
current=0

for model_path in "${model_paths[@]}"; do
  for eval_topic in "${eval_topics[@]}"; do
    for party_num in "${party_nums[@]}"; do
      for task_setting in "${task_settings[@]}"; do
        for voting_threshold_setting in "${voting_threshold_settings[@]}"; do
          current=$((current + 1))
          percentage=$((current * 100 / total_tasks))
          printf "\rProgress: [%-50s] %d%%" $(printf "#%.0s" $(seq 1 $((percentage/2)))) $percentage
          python runner/task_runner.py \
            --task_setting "task_setting" \
            --voting_threshold_setting "$voting_threshold_setting" \
            --eval_topic "$eval_topic" \
            --party_num "$party_num" \
            --model_name_or_path "$model_path" \
            --multi_gpu
        done
      done
    done
  done
done

echo -e "\nDone!"</edit>
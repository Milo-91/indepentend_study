python run.py \
    --task game24 \
    --task_start_index 900 \
    --task_end_index 950 \
    --method_generate propose \
    --method_evaluate value \
    --method_select greedy \
    --n_evaluate_sample 3 \
    --n_select_sample 3 \
    --k 5 \
    --algorithm 'fsd_graph' \
    --name_of_task $(date +%Y-%m-%d)
    ${@}

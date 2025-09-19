check:
	uv run ./tools/check_data.py ./data_1107/5g/

	uv run ./tools/check_data.py ./data_1107/unseen/

	uv run ./tools/check_data.py ./data_1107/microwave/

	uv run ./tools/check_data.py ./data_1107/low_frequency/

	uv run ./tools/check_data.py ./data_1107/baseline/

train:
	uv run .\semg_train_mlp.py
	
run_test:
	uv run ./semg_infer_mlp.py --mode offline --csv ./data_1107/baseline/*.csv >> results.md

	uv run ./semg_infer_mlp.py --mode offline --csv "./data_1107/unseen/*.csv" >> results.md

	uv run ./semg_infer_mlp.py --mode offline --csv "./data_1107/laser/*.csv" >> results.md

	uv run ./semg_infer_mlp.py --mode offline --csv "./data_1107/microwave/*.csv" >> results.md

	uv run ./semg_infer_mlp.py --mode offline --csv ./data_1107/5g/*.csv >> results.md

	uv run ./semg_infer_mlp.py --mode offline --csv "./data_1107/low_frequency/*.csv" >> results.md

	uv run ./semg_infer_mlp.py --mode offline --csv "./data_1107/bass25hz/*.csv" >> results.md

	uv run ./semg_infer_mlp.py --mode offline --csv "./data_1107/bass20hz/*.csv" >> results.md
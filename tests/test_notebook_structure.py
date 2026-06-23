import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebook_full_model.ipynb"
BACKUP = ROOT / "backups" / "notebook_full_model_original.ipynb"


def _load_notebook():
    return json.loads(NOTEBOOK.read_text(encoding="utf-8"))


def _markdown_text(notebook):
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "markdown"
    )


def _code_text(notebook):
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
    )


def _first_code_cell_containing(notebook, phrase):
    for idx, cell in enumerate(notebook["cells"]):
        if cell.get("cell_type") != "code":
            continue
        if phrase in "".join(cell.get("source", [])):
            return idx
    return None


def test_original_notebook_backup_exists():
    assert BACKUP.exists(), "Keep an untouched backup before rewriting the teaching notebook."


def test_teaching_notebook_contains_theory_sections():
    markdown = _markdown_text(_load_notebook())
    required_phrases = [
        "Darcy equation and mixed formulation",
        "GMsFEM multiscale basis functions",
        "Learning problem for a neural operator",
        "Network architecture",
        "What you should save",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in markdown]
    assert not missing, f"Missing teaching sections: {missing}"


def test_notebook_has_quick_run_controls_and_outputs():
    code = _code_text(_load_notebook())
    required_code = [
        "RUN_MODE =",
        "quick",
        "QUICK_TRAIN_SIZE",
        "QUICK_EPOCHS",
        "RESULTS_DIR",
        "save_summary",
    ]
    missing = [phrase for phrase in required_code if phrase not in code]
    assert not missing, f"Missing runnable teaching controls: {missing}"


def test_notebook_has_no_obvious_mojibake():
    markdown = _markdown_text(_load_notebook())
    suspicious = ["杩", "涓", "锛", "瀹", "棰"]
    found = [token for token in suspicious if token in markdown]
    assert not found, f"Notebook markdown still contains likely mojibake: {found}"


def test_theory_sections_use_tex_math_not_inline_code():
    notebook = _load_notebook()
    theory_text = "\n".join(
        "".join(notebook["cells"][idx].get("source", []))
        for idx in [1, 2, 3, 4]
    )
    assert "`" not in theory_text, "Use TeX math in theory sections instead of inline-code math."
    required_tex = [
        r"\kappa",
        r"\nabla",
        r"\operatorname{div}",
        r"\lambda",
        r"\phi",
        r"\mathcal{G}",
        r"\mathcal{N}_{\theta}",
    ]
    missing = [token for token in required_tex if token not in theory_text]
    assert not missing, f"Missing expected TeX notation: {missing}"


def test_r2_score_is_defined_before_evaluation_helper():
    notebook = _load_notebook()
    code = _code_text(notebook)
    r2_pos = code.find("def batch_r2_score")
    eval_pos = code.find("def evaluate_model_on_loader")
    assert r2_pos != -1, "batch_r2_score must be defined in the notebook."
    assert eval_pos != -1, "evaluate_model_on_loader must be defined in the notebook."
    assert r2_pos < eval_pos, "Define batch_r2_score before evaluate_model_on_loader uses it."


def test_spectral_analysis_is_not_in_first_training_notebook():
    markdown = _markdown_text(_load_notebook()).lower()
    code = _code_text(_load_notebook()).lower()
    assert "optional single-basis spectral check" not in markdown
    assert "plot_single_basis_spectrum" not in code
    assert "radial_power_spectrum" not in code

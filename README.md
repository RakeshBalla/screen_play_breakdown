
# screen_play_breakdown

## Project Overview
This project focuses on scene breakdowns using different recognition models. It supports tasks like structure recognition and product recognition, with options for segmentation and different models.

---

## Installation
Ensure you have Python 3.11 installed. Then, clone the repository:

```bash
git clone https://github.com/RakeshBalla/screen_play_breakdown.git
```

Navigate to the source directory:

```bash
cd screen_play_breakdown/llm_main/src
```

---

## Configuration
Define the following constants in your environment or script:

```python
task_name = "prod_recog"  # Options: "structure_recognition", "prod_recog"
segregate_folder = False  # True or False
model_name = "deepseek"   # Options: "openai", "gemini", "deepseek"
```

---

## Modules

### Module 1: Scene Breakdown
This module handles both product recognition and structure recognition.

#### Component 1: Validation (used for both product and structure recognition)
- **Inputs:**
  - Input CSV:
    ```python
    csv_path = "/home/ntlpt19/personal_projects/screen_play_breakdown_project/screen_data/testing_jun10/AK_all_scenes.csv"
    ```
  - Output JSON Directory:
    ```python
    output_json_dir = "/home/ntlpt19/personal_projects/screen_play_breakdown_project/screen_data/testing_jun10/ak_outputs_deepseek"
    ```
- **Process:**
  ```bash
  python -m validation.test_scenes
  ```

- **Ground Truth Validation:**
  - CSV Path:
    ```python
    csv_path = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/testing_jun10/prod_reco_gt.csv"
    ```
  - Output Directory:
    ```python
    output_json_dir = "/home/ntlpt19/personal_projects/screen_play_breakdown/data/testing_jun10/outputs"
    ```
  - Output Metrics CSV:
    ```python
    output_csv_path = "metrics_output.csv"
    ```
  - Command:
    ```bash
    python -m validation.test_scenes_gt
    ```

#### Component 2: Scene Data from PDFs (full data)
- **Purpose:** Use when scenes data are PDFs stored under folder categories (`large`, `medium`, `small`)
- **Input Format:**
  - Data folder contains subfolders like `large`, `medium`, `small`.

- **Execution example:**
  ```bash
  python -m screenplay_breakdown.src.main --master_folder "/home/ntlpt19/personal_projects/screen_play_breakdown_project/screen_data/data/testing_samples/data/medium" --output_folder "/home/ntlpt19/personal_projects/screen_play_breakdown_project/screen_data/large_small_me_out"
  ```

---

## Additional Notes
- Make sure to adjust paths and parameters according to your environment.
- For different tasks, modify `task_name` and other constants as needed.
- The modules support validation, scene processing, and analysis tailored to your scene and data structure.


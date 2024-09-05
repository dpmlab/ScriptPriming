This repository contains code and data for:
Soares et al. "Top-down attention shifts behavioral and neural event boundaries in narratives with overlapping event scripts." Current Biology, 2024.

Directory contents:
* behavior: Data and code for behavioral measures
   * online_memory_data.csv and fMRI_memory_data.csv: short answer responses for each story
   * fMRI_SA.csv and online_SA.csv: scored accuracies for short answers
   * analyze_SA.Rmd: analysis of short answer performance
   * online_boundary_data.csv: event boundary responses (collected from online participants only)
   * comparison_A_Priori_Boundaries.ipynb: compares boundary responses to story boundaries, producing comparison_to_EB_vals.csv, which is analyzed and plotted by boundaries.Rmd
   * within_Group_Synchronization.ipynb: compares boundary responses between participants
 * fMRI: Code for fMRI analyses
   * VizStories.ipynb: generates visualization and statistics for story stimuli
   * TargetSents.ipynb: generates target_TRs.pickle with the timing of target sentences (with information that will be tested later in the short answer questions)
   * StoryComparison_ROI_perms.py: computes the schema effects (and corresponding null distributions) for all ROIs, producing StoryComparison_roi_vals_perms and StoryComparison_roi_vals_mismatch_perms, which are analyzed by StoryComparison_ROI_analyze_perms.ipynb
   * HMM.ipynb: HMM event boundary analyses
   * Hipp.ipynb: Supplemental analyses of Hippocampal activity
* story_csv: Full texts of each story

Additional resources for this paper are available:
* [fMRI data in BIDS format](https://doi.org/10.18112/openneuro.ds004631.v1.0.0)
* [Audio recordings of story stimuli](https://figshare.com/projects/Script_Combination_Stories/168656)

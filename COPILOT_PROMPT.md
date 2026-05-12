# Copilot / agent prompt

Use the following message after uploading the files to GitHub if you want Copilot or another coding agent to polish the repository.

```text
@copilot Please organize and polish this repository so it becomes a clean, professional GitHub project.

Context:
- This is a computational astrophysics project about gravitational lensing.
- The repository already includes the Python code, documentation, and the selected figures.
- Do not add the original PDF; it was used only as background material while preparing the new Markdown documents.

Required final structure:
.
├── README.md
├── PROJECT_INFO.md
├── COPILOT_PROMPT.md
├── REFERENCES.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── circular_galaxy_sis.py
│   ├── elliptical_galaxy_sis.py
│   ├── spiral_galaxy_sis.py
│   └── README.md
├── docs/
│   ├── theory_and_background.md
│   ├── results_and_discussion.md
│   └── implementation_notes.md
└── assets/
    ├── ASSETS_INDEX.md
    └── figures/
        ├── simulations/
        ├── observations/
        ├── parameter_studies/
        └── special_cases/

Tasks:
1. Keep the repository structure above.
2. Preserve the long-form documentation already written in the Markdown files.
3. Make README.md the main landing page of the repository.
4. Ensure all relative links to images and documents work correctly on GitHub.
5. Keep the scientific content intact: do not alter the equations or claim results that are not supported by the figures.
6. Do not reintroduce the original PDF.
7. Keep the project in English, except for captions embedded inside the already existing figures.
8. If needed, lightly improve grammar, formatting and Markdown layout.
9. Preserve the cautionary note that the spiral case is exploratory.
10. Leave the repository ready for a clean commit.

Suggested commit message:
Add gravitational lensing documentation, figures and code organization
```

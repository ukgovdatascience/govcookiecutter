@echo off


IF /I "%1"==".DEFAULT_GOAL " GOTO .DEFAULT_GOAL 
IF /I "%1"=="requirements" GOTO requirements
IF /I "%1"=="prepare_docs_folder" GOTO prepare_docs_folder
IF /I "%1"=="docs" GOTO docs
IF /I "%1"=="docs_check_external_links" GOTO docs_check_external_links
IF /I "%1"=="help" GOTO help
GOTO error

:.DEFAULT_GOAL 
	CALL make.bat =
	CALL make.bat help
	GOTO :EOF

:requirements
	python3 -m pip install -U pip setuptools
	python3 -m pip install -r requirements.txt
	pre-commit install
	GOTO :EOF

:prepare_docs_folder
	if [ ! -d "./docs/_build" ]; then mkdir ./docs/_build; fi
	find ./docs/_build -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} \;
	GOTO :EOF

:docs
	CALL make.bat prepare_docs_folder
	CALL make.bat requirements
	sphinx-build -b html ./docs ./docs/_build
	GOTO :EOF

:docs_check_external_links
	CALL make.bat prepare_docs_folder
	CALL make.bat requirements
	sphinx-build -b linkcheck ./docs ./docs/_build
	GOTO :EOF

:help
	@echo "$%tput bold%Available rules:$%tput sgr0%"
	@echo
	@sed -n -e "/^
	h; s/.*//; :doc" -e "H; n; s/^
	t doc" -e "s/:.*//; G; s/\\n
	s/\\n/ /g; p; }" %MAKEFILE_LIST% | LC_ALL='C' sort --ignore-case | awk -F '---' -v ncol=$%tput cols% -v indent=25 -v col_on="$%tput setaf 6%" -v col_off="$%tput sgr0%" '{ printf "%s%*s%s ", col_on, -indent, $$1, col_off; n = split($$2, words, " "); line_length = ncol - indent; for (i = 1; i <= n; i++) { line_length -= length(words[i]) + 1; if (line_length <= 0) { line_length = ncol - indent - length(words[i]) - 1; printf "\n%*s ", -indent, " "; } printf "%s ", words[i]; } printf "\n"; }' | more %shell test $(shell uname% = Darwin && echo '--no-init --raw-control-chars')
	GOTO :EOF

:error
    IF "%1"=="" (
        ECHO make: *** No targets specified and no makefile found.  Stop.
    ) ELSE (
        ECHO make: *** No rule to make target '%1%'. Stop.
    )
    GOTO :EOF

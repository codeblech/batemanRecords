documentation:
	@(poetry export --with docs -f requirements.txt -o requirements-docs.txt; cd docs; make html)

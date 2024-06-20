all:

test:
	pytest tests -s

html:
	cd docs; make html

clean:
	rm -rf apps/__pycache__ ipose/__pycache__  tests/__pycache__ .pytest_cache

cleandoc:
	cd docs; make clean

cleanall: clean cleandoc

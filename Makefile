all:

test:
	pytest tests -s

html:
	cd docs; make html

clean:
	rm -rf ipose/__pycache__  tests/__pycache__ .pytest_cache 

cleandoc:
	cd docs; make clean

cleanall: clean cleandoc

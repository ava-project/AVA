default:
	@echo "make install -> to install"
	@echo "make run -> to run the project"
	@echo "make dist -> to bundle"

install:
	pip3 install -r requirements.txt

run:
	python3.6 -m ava

dist:
	python3.6 setup.py build

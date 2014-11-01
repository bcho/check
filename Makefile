.PHONY: clean
clean:
	rm -rf dist build *.egg-info
	find . -name '__pycache__' | xargs rm -rf

.PHONY: test
test:
	py.test

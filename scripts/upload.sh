#!/bin/sh
# Set TWINE_PASSWORD to the pip password

TEST_REPOSITORY=""

if [ $TEST = "true" ]; then
	TEST_REPOSITORY="--repository-url https://test.pypi.org/legacy/"
fi

twine upload \
	$TEST_REPOSITORY \
	dist/* \
	-u cleanunicorn

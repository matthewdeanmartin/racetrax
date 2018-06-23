#!/usr/bin/env bash
#!/usr/bin/env bash

PROJECT_NAME=racetrax
run()
{
    echo Running lint...
    rm -f lint.txt

    # now everything is in 1 module
    # --load-plugins pylint_django

    if [ ! -f pylintrc.ini ]; then
        pylint --generate-rcfile>pylintrc.ini
    fi
    # pylint always returns a failure code. But
    # there is no way anyone wants to always fix all lint.
    ./lint_it.sh --rcfile=pylintrc.ini "${PROJECT_NAME}">lint.txt || exit 0
}
run
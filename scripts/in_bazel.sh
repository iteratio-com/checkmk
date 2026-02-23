#!/usr/bin/env bash

if [[ $# -ne 2 && $# -ne 3 ]]; then
    echo "Usage: $0 <EXTENSION> <KIND> [<LIMIT>]" >&2
    exit 1
fi

ext=$1
kind=$2
limit=${3:-0}

out=$(
    comm -23 \
        <(git ls-files "*\.$ext" ":!doc/*" | sort) \
        <(
            bazel cquery '
            kind("source file", deps(kind("'"$kind"'", //...)))
        ' |
                grep -E "\.$ext " |
                sed -E 's| \([^)]*\)$||; s|^//([^:]+):|\1/|' |
                sort
        )
)

count=$(echo "$out" | wc -l)
echo "Found $count \".$ext\" files not declared as $kind"
echo "-----"
echo "$out"

if ((count > limit)); then
    exit 1
fi

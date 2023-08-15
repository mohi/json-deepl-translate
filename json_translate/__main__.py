#!/usr/bin/env python
# -*- coding: utf-8 -*-
from parser import get_parser
from languages import get_target_lang_code
from files import (
    get_input_dir_from_file,
    get_json_file_name_from_input_file,
    get_input_file_from_dir,
    get_output_file,
    save_results_file,
)
from translators.deepl import DeepLTranslator
import json


def main():
    parser = get_parser("json_translate")
    args = parser.parse_args()

    input_dir = get_input_dir_from_file(args.file)
    input_file = get_input_file_from_dir(input_dir)
    lang_code = get_target_lang_code(args.locale)
    json_file_name = get_json_file_name_from_input_file(input_file)
    ext_source_file = get_input_file_from_dir(get_input_dir_from_file(args.extend))
    # print(ext_source_file, type(ext_source_file))
    if lang_code.lower() == json_file_name.lower():
        print("You are trying to translate the same language!")
        exit(1)

    output_file = get_output_file(
        output=args.output, lang_code=lang_code, input_file=input_file
    )
    with open(input_file, "r", encoding=args.encoding) as f:
        input_data = json.load(f)
    if ext_source_file:
        # read extend file
        with open(ext_source_file, "r", encoding=args.encoding) as f:
            ext_data = json.load(f)
        # remove extend keys from input file 
        input_data = dict([(key, value) for key, value in input_data.items() if (ext_data.get(key) is None or ext_data.get(key) == "")])
        # pass that to translate_file

    translator = DeepLTranslator(
        target_locale=lang_code.upper(),
        source_locale=args.source_locale,
        glossary=args.glossary,
        sleep=args.sleep,
        skip=args.skip,
        encoding=args.encoding,
        log_translations=args.log,
    )
    results = translator.iterate_over_keys(data=input_data)
    if ext_source_file:
        results = dict([(key, results.get(key)) if (ext_data.get(key) is None or ext_data.get(key) == "") else (key, value) for key, value in ext_data.items()])
        # add extend file to results
    save_results_file(
        data=results,
        output_file=output_file,
        indent=args.indent,
        encoding=args.encoding,
    )


if __name__ == "__main__":
    main()

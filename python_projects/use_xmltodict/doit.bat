@rem Use 'python create_json.py' to build outfile.json
@python directions.py outfile.json test.html
@tidy -i test.html > test2.html

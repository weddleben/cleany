from cleany.cli import main

main()

'''
python3 -m nuitka compile.py \                 
  --standalone \
  --onefile \
  --output-filename=cleany \
  --onefile-tempdir-spec="{CACHE_DIR}/cleany"
  '''
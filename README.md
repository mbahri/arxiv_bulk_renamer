# arxiv_bulk_renamer
Bulk renames PDFs of arXiv papers recursively + finds duplicates

## Usage

Place the script at the root of a directory containing PDF files whose names begin by an arXiv paper identified (xxxx.yyyyy).
Run
```
python bulk_rename_arxiv.py
```
The script will recursively probe the directory for PDFs, query the list of ids to get paper names, and rename all files.
If any duplicates are found, the list of duplicate files will be printed at the end.

**Warning: The script will not ask for user confirmation at any point, use at your own risk!**